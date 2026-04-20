"""
Module 1: Search Automation
Automated searching for candidates on GitHub and LinkedIn (via Google).
Target: Extract candidate profiles with name, URL, role, location, skills.
"""

import requests
import json
import time
import csv
from datetime import datetime
from typing import List, Dict, Set
from urllib.parse import quote
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.audit_log import log_sourcing_action

class SearchAutomation:
    def __init__(self, role_config: Dict):
        """
        Initialize search automation with role configuration.

        Args:
            role_config: Dict with required_skills, github_search_queries, etc.
        """
        self.role = role_config.get('title', 'Unknown Role')
        self.config = role_config
        self.candidates = []
        self.seen_urls = set()  # For deduplication
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Coco-Sourcing-Bot/1.0'
        })

    def search_github(self) -> List[Dict]:
        """
        Search GitHub for candidates using the free public API.
        Searches by: language + location + repo keywords
        Returns: List of candidate profiles
        """
        print(f"\n🔍 Searching GitHub for {self.role}...")

        candidates = []
        github_api_base = "https://api.github.com/search/users"

        for query in self.config.get('github_search_queries', []):
            try:
                # GitHub API search: language:python location:Pakistan type:user
                # Convert role-specific queries to GitHub API format
                github_query = self._convert_to_github_query(query)

                print(f"  Query: {github_query}")

                params = {
                    'q': github_query,
                    'per_page': 30,
                    'sort': 'repositories',
                    'order': 'desc'
                }

                response = self.session.get(github_api_base, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    results_count = len(data.get('items', []))

                    # Log the search
                    log_sourcing_action(
                        platform="GitHub",
                        query=github_query,
                        results_found=results_count,
                        context="github_api_search"
                    )

                    for user in data.get('items', []):
                        # Fetch detailed profile for each user
                        profile = self._fetch_github_profile(user['login'])
                        if profile:
                            candidates.append(profile)
                else:
                    print(f"  ⚠️  GitHub API returned {response.status_code}")

                # Rate limiting: wait before next query
                time.sleep(2)

            except Exception as e:
                print(f"  ❌ Error searching GitHub for '{query}': {str(e)}")

        print(f"  ✅ Found {len(candidates)} candidates on GitHub")
        return candidates

    def search_linkedin_via_google(self) -> List[Dict]:
        """
        Search LinkedIn profiles via Google (site:linkedin.com queries).
        Returns: List of candidate profiles
        """
        print(f"\n🔍 Searching LinkedIn via Google for {self.role}...")

        candidates = []

        for query in self.config.get('linkedin_search_queries', []):
            try:
                print(f"  Query: {query}")

                # Use Google Custom Search or parse Google results
                # For now, we'll log the query and note it for manual review
                # (Automated Google scraping is rate-limited; recommend manual Google search)

                log_sourcing_action(
                    platform="LinkedIn (Google)",
                    query=query,
                    results_found=0,  # Placeholder
                    context="linkedin_google_search"
                )

                # TODO: Implement Google Custom Search API integration if available
                # For MVP, we'll recommend manual Google search or use Selenium
                print(f"    Note: LinkedIn via Google requires manual search or paid API")
                print(f"    → Copy this query to Google: {query}")

            except Exception as e:
                print(f"  ❌ Error: {str(e)}")

        return candidates

    def search_google(self) -> List[Dict]:
        """
        General Google search for candidates.
        Note: Automated Google scraping is rate-limited.
        Returns: List of candidate profiles (URLs only for manual review)
        """
        print(f"\n🔍 Preparing Google searches for {self.role}...")

        candidates = []

        for query in self.config.get('google_search_queries', []):
            try:
                print(f"  Query: {query}")

                log_sourcing_action(
                    platform="Google",
                    query=query,
                    results_found=0,  # Placeholder
                    context="google_organic_search"
                )

                # Log for user to manually search
                print(f"    → Recommended manual Google search (automated scraping blocked)")
                print(f"    → Query: {query}")

            except Exception as e:
                print(f"  ❌ Error: {str(e)}")

        return candidates

    def _convert_to_github_query(self, role_query: str) -> str:
        """
        Convert a role-specific query to GitHub API format.
        Example: "EdTech product management" → "python location:Pakistan type:user"
        """
        # Map keywords to GitHub language/topic tags
        keywords_to_lang = {
            'product': 'python OR javascript',
            'ai': 'python',
            'ml': 'python',
            'ux': 'javascript OR typescript',
            'design': 'javascript',
            'edtech': 'python OR javascript',
            'education': 'python OR javascript'
        }

        language = 'python OR javascript'  # Default
        for keyword, lang in keywords_to_lang.items():
            if keyword.lower() in role_query.lower():
                language = lang
                break

        # Build GitHub API query: language + location
        github_query = f"{language} location:Pakistan type:user stars:>10"
        return github_query

    def _fetch_github_profile(self, username: str) -> Dict:
        """
        Fetch detailed GitHub user profile.
        Returns: Dict with user info or None if error
        """
        try:
            response = self.session.get(f"https://api.github.com/users/{username}", timeout=10)

            if response.status_code == 200:
                data = response.json()

                profile = {
                    'name': data.get('name', username),
                    'github_url': data.get('html_url'),
                    'github_username': username,
                    'bio': data.get('bio', ''),
                    'location': data.get('location', ''),
                    'company': data.get('company', ''),
                    'public_repos': data.get('public_repos', 0),
                    'followers': data.get('followers', 0),
                    'email': data.get('email'),  # Only public emails
                    'source': 'GitHub',
                    'linkedin_url': None,
                    'confidence': 'medium'
                }

                # Check if profile looks relevant (has repos, followers, location)
                if profile['public_repos'] > 0 and 'pakistan' in (profile['location'] or '').lower():
                    return profile

        except Exception as e:
            print(f"    Error fetching {username}: {str(e)}")

        return None

    def deduplicate_candidates(self, candidates: List[Dict]) -> List[Dict]:
        """
        Remove duplicate candidates based on email or URL.
        """
        unique_candidates = []
        seen = set()

        for candidate in candidates:
            # Create unique identifier from email or GitHub URL
            unique_id = (
                candidate.get('email') or
                candidate.get('github_url') or
                candidate.get('linkedin_url')
            )

            if unique_id and unique_id not in seen:
                seen.add(unique_id)
                unique_candidates.append(candidate)

        return unique_candidates

    def run_all_searches(self) -> List[Dict]:
        """
        Execute all search layers (GitHub → LinkedIn → Google).
        Returns: Combined list of unique candidates
        """
        print(f"\n{'='*60}")
        print(f"SOURCING AUTOMATION: {self.role}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        all_candidates = []

        # Layer 1: GitHub (most reliable for free)
        github_candidates = self.search_github()
        all_candidates.extend(github_candidates)

        # Layer 2: LinkedIn via Google (manual or API-based)
        linkedin_candidates = self.search_linkedin_via_google()
        all_candidates.extend(linkedin_candidates)

        # Layer 3: General Google (manual or API-based)
        google_candidates = self.search_google()
        all_candidates.extend(google_candidates)

        # Deduplicate
        unique_candidates = self.deduplicate_candidates(all_candidates)

        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Total candidates found: {len(unique_candidates)}")
        print(f"Target: {self.config.get('target_count', 50)}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        return unique_candidates


def load_role_config(role_slug: str) -> Dict:
    """Load role configuration from config/role_profiles.json"""
    config_path = os.path.join(
        os.path.dirname(__file__),
        '../../config/role_profiles.json'
    )

    with open(config_path, 'r') as f:
        all_roles = json.load(f)

    if role_slug not in all_roles:
        raise ValueError(f"Role '{role_slug}' not found in config")

    return all_roles[role_slug]


def save_raw_candidates_csv(candidates: List[Dict], role_slug: str) -> str:
    """
    Save raw candidates to CSV.
    Returns: Path to CSV file
    """
    output_dir = os.path.join(
        os.path.dirname(__file__),
        f'../../output/sourcing/automation/{role_slug}'
    )
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    csv_path = os.path.join(output_dir, f'{timestamp}-raw-candidates.csv')

    if candidates:
        fieldnames = list(candidates[0].keys())
    else:
        fieldnames = ['name', 'github_url', 'linkedin_url', 'location', 'source']

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"✅ Saved {len(candidates)} candidates to {csv_path}")
    return csv_path


if __name__ == '__main__':
    # Test: Search for Soul Architect candidates

    try:
        role_config = load_role_config('soul-architect')
        searcher = SearchAutomation(role_config)
        candidates = searcher.run_all_searches()

        # Save to CSV
        csv_path = save_raw_candidates_csv(candidates, 'soul-architect')

        print(f"\n✅ Search complete! Results saved to: {csv_path}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
