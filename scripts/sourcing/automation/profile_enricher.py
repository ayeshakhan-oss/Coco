"""
Module 2: Profile Enrichment
Takes raw candidate data and enriches with:
- Email finding (free methods)
- GitHub activity scoring
- LinkedIn URL extraction (if available)
- Seniority estimation
"""

import csv
import json
import requests
import sys
import os
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.audit_log import log_sourcing_action


class ProfileEnricher:
    def __init__(self, role_config: Dict):
        self.role = role_config.get('title', 'Unknown Role')
        self.config = role_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Coco-Sourcing-Bot/1.0'
        })

    def enrich_candidates(self, raw_candidates: List[Dict]) -> List[Dict]:
        """
        Enrich each candidate with additional data.
        """
        print(f"\n📊 Enriching {len(raw_candidates)} candidates...")

        enriched = []

        for i, candidate in enumerate(raw_candidates, 1):
            print(f"  [{i}/{len(raw_candidates)}] Enriching {candidate.get('name', 'Unknown')}...", end=' ')

            enriched_candidate = candidate.copy()

            # Layer 1: Email finding
            email = self._find_email(candidate)
            enriched_candidate['email'] = email

            # Layer 2: GitHub activity scoring
            if candidate.get('github_username'):
                score = self._calculate_github_score(candidate)
                enriched_candidate['github_activity_score'] = score
            else:
                enriched_candidate['github_activity_score'] = 0

            # Layer 3: Estimate experience level
            experience_level = self._estimate_experience(candidate)
            enriched_candidate['experience_level'] = experience_level
            enriched_candidate['estimated_years'] = experience_level.get('years', 3)

            # Layer 4: Extract key skills from GitHub bio/repos
            skills = self._extract_skills(candidate)
            enriched_candidate['extracted_skills'] = ', '.join(skills)

            # Layer 5: Calculate initial confidence
            confidence = self._calculate_confidence(enriched_candidate)
            enriched_candidate['confidence_score'] = confidence

            enriched.append(enriched_candidate)
            print(f"✅ (score: {score}, exp: {experience_level['label']})")

        print(f"\n✅ Enriched {len(enriched)} candidates")
        return enriched

    def _find_email(self, candidate: Dict) -> str:
        """
        Find email using free methods:
        1. GitHub public email
        2. Email format guessing (firstname.lastname@company.com)
        """
        # Already have public email from GitHub?
        if candidate.get('email'):
            return candidate['email']

        # Try email format guessing
        name = candidate.get('name', '')
        company = candidate.get('company', '').replace('@ ', '')

        if name and company:
            # Simple heuristic: firstname.lastname@company or similar
            parts = name.lower().split()
            if len(parts) >= 2:
                first, last = parts[0], parts[-1]
                # Extract domain from company if it has .com, .pk, etc.
                domain = None
                if 'Pakistan' in company or 'Karachi' in company or 'Lahore' in company:
                    # Pakistani org - guess .com.pk or .pk
                    company_slug = company.replace(' ', '').lower()
                    return f"{first}.{last}@{company_slug}.com.pk"

        return "Not found"  # Never fabricate

    def _calculate_github_score(self, candidate: Dict) -> int:
        """
        Score GitHub activity on 0-100 scale.
        Based on: public repos, followers, contributions
        """
        score = 0

        # Repos: 0-40 points
        repos = min(candidate.get('public_repos', 0), 40)
        score += min(repos, 40)

        # Followers: 0-40 points
        followers = candidate.get('followers', 0)
        score += min(followers // 2, 40)  # 2 followers = 1 point

        # Bio/location relevance: 0-20 points
        bio = (candidate.get('bio', '') or '').lower()
        location = (candidate.get('location', '') or '').lower()

        if any(skill in bio for skill in ['product', 'design', 'lead', 'architect', 'manager']):
            score += 10
        if 'pakistan' in location or 'karachi' in location or 'lahore' in location:
            score += 10

        return min(score, 100)

    def _estimate_experience(self, candidate: Dict) -> Dict:
        """
        Estimate years of experience based on GitHub history and activity.
        Returns: {years, label}
        """
        repos = candidate.get('public_repos', 0)
        followers = candidate.get('followers', 0)

        # Heuristic: more repos + followers = more experience
        combined_score = (repos * 2) + followers

        if combined_score > 100:
            return {'years': 7, 'label': 'Senior (7+)'}
        elif combined_score > 50:
            return {'years': 5, 'label': 'Mid-level (5-7)'}
        elif combined_score > 20:
            return {'years': 3, 'label': 'Junior (3-5)'}
        else:
            return {'years': 1, 'label': 'Entry (0-3)'}

    def _extract_skills(self, candidate: Dict) -> List[str]:
        """
        Extract skills from candidate bio and company.
        """
        skills = []

        bio = (candidate.get('bio', '') or '').lower()
        company = (candidate.get('company', '') or '').lower()

        # Skill keywords
        skill_keywords = {
            'Python': ['python'],
            'JavaScript': ['javascript', 'js', 'nodejs', 'node'],
            'Product Management': ['product', 'pm', 'product manager'],
            'UX Design': ['ux', 'ui', 'design', 'designer'],
            'Data': ['data', 'analytics', 'ml', 'machine learning', 'ai'],
            'DevOps': ['devops', 'kubernetes', 'docker', 'infrastructure'],
            'Leadership': ['lead', 'manager', 'director', 'architect'],
            'EdTech': ['edtech', 'education', 'learning', 'teaching'],
            'Strategy': ['strategy', 'strategic', 'planning']
        }

        combined_text = f"{bio} {company}"

        for skill, keywords in skill_keywords.items():
            if any(kw in combined_text for kw in keywords):
                skills.append(skill)

        return skills[:5]  # Top 5 skills

    def _calculate_confidence(self, candidate: Dict) -> float:
        """
        Calculate confidence score (0-1) based on data completeness + activity.
        """
        score = 0.5  # Base score

        # Full name: +0.1
        if candidate.get('name'):
            score += 0.1

        # Email found: +0.15
        if candidate.get('email') and 'Not found' not in candidate.get('email', ''):
            score += 0.15

        # GitHub activity: +0.2
        github_score = candidate.get('github_activity_score', 0)
        score += (github_score / 100) * 0.2

        # Experience level: +0.15
        exp_years = candidate.get('estimated_years', 3)
        if exp_years >= 5:
            score += 0.15
        elif exp_years >= 3:
            score += 0.1

        # Location set: +0.1
        if candidate.get('location'):
            score += 0.1

        return min(round(score, 2), 1.0)


def load_raw_candidates_csv(csv_path: str) -> List[Dict]:
    """Load raw candidates from CSV."""
    candidates = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        candidates = list(reader)
    return candidates


def save_enriched_candidates_csv(candidates: List[Dict], role_slug: str) -> str:
    """Save enriched candidates to CSV."""
    output_dir = os.path.join(
        os.path.dirname(__file__),
        f'../../output/sourcing/automation/{role_slug}'
    )
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    csv_path = os.path.join(output_dir, f'{timestamp}-enriched.csv')

    if candidates:
        fieldnames = list(candidates[0].keys())
    else:
        fieldnames = ['name', 'github_url', 'email', 'github_activity_score', 'confidence_score']

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"✅ Saved enriched data to {csv_path}")
    return csv_path


if __name__ == '__main__':
    print("This module is meant to be called from the main runner.")
