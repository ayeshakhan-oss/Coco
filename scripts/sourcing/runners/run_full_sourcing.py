#!/usr/bin/env python3
"""
SOURCING AUTOMATION SUITE — Main Runner

Orchestrates all three modules:
  Module 1: Search Automation (GitHub + LinkedIn via Google)
  Module 2: Profile Enrichment (Email + GitHub scoring)
  Module 3: Tier Classification + Excel Generation

Usage:
  python run_full_sourcing.py --role soul-architect --target 50

Output:
  output/sourcing/automation/[role]/
    ├── [date]-raw-candidates.csv
    ├── [date]-enriched.csv
    └── [date]-FINAL.xlsx
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sourcing.automation.search_automation import SearchAutomation, load_role_config, save_raw_candidates_csv
from sourcing.automation.profile_enricher import ProfileEnricher, load_raw_candidates_csv, save_enriched_candidates_csv
from sourcing.automation.tier_classifier_and_excel import TierClassifier, ExcelGenerator
from utils.audit_log import log_sourcing_action


def main():
    parser = argparse.ArgumentParser(
        description='Run Sourcing Automation Suite for a specific role'
    )
    parser.add_argument(
        '--role',
        required=True,
        help='Role slug (e.g., soul-architect)'
    )
    parser.add_argument(
        '--target',
        type=int,
        default=50,
        help='Target number of candidates (default: 50)'
    )
    parser.add_argument(
        '--skip-search',
        action='store_true',
        help='Skip search phase, use existing raw CSV'
    )

    args = parser.parse_args()

    print("\n" + "="*70)
    print("SOURCING AUTOMATION SUITE v1.0")
    print("="*70)
    print(f"Role: {args.role}")
    print(f"Target: {args.target} candidates")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

    try:
        # Load role configuration
        print("📋 Loading role configuration...")
        role_config = load_role_config(args.role)
        role_config['target_count'] = args.target
        print(f"✅ Loaded: {role_config.get('title', args.role)}")

        # =========================================================================
        # MODULE 1: SEARCH AUTOMATION
        # =========================================================================
        if not args.skip_search:
            print("\n" + "-"*70)
            print("MODULE 1: SEARCH AUTOMATION")
            print("-"*70)

            searcher = SearchAutomation(role_config)
            raw_candidates = searcher.run_all_searches()

            if not raw_candidates:
                print("⚠️  No candidates found from automated searches.")
                print("💡 Tip: You can manually add candidates to the raw CSV and rerun Module 2-3.")
                raw_candidates = []

            raw_csv_path = save_raw_candidates_csv(raw_candidates, args.role)
        else:
            print("\n⏭️  Skipping search phase...")
            # Find existing raw CSV
            output_dir = os.path.join(
                os.path.dirname(__file__),
                f'../../output/sourcing/automation/{args.role}'
            )
            if not os.path.exists(output_dir):
                print(f"❌ No existing data found in {output_dir}")
                sys.exit(1)

            # Use most recent raw CSV
            import glob
            raw_files = sorted(glob.glob(os.path.join(output_dir, '*-raw-candidates.csv')), reverse=True)
            if not raw_files:
                print(f"❌ No raw CSV files found in {output_dir}")
                sys.exit(1)

            raw_csv_path = raw_files[0]
            print(f"✅ Using existing: {raw_csv_path}")
            raw_candidates = load_raw_candidates_csv(raw_csv_path)

        # =========================================================================
        # MODULE 2: PROFILE ENRICHMENT
        # =========================================================================
        print("\n" + "-"*70)
        print("MODULE 2: PROFILE ENRICHMENT")
        print("-"*70)

        enricher = ProfileEnricher(role_config)
        enriched_candidates = enricher.enrich_candidates(raw_candidates)

        enriched_csv_path = save_enriched_candidates_csv(enriched_candidates, args.role)

        # =========================================================================
        # MODULE 3: TIER CLASSIFICATION & EXCEL GENERATION
        # =========================================================================
        print("\n" + "-"*70)
        print("MODULE 3: TIER CLASSIFICATION & EXCEL GENERATION")
        print("-"*70)

        classifier = TierClassifier(role_config)
        tiered_candidates = classifier.classify_candidates(enriched_candidates)

        excel_gen = ExcelGenerator(role_config)
        excel_path = excel_gen.generate_excel(tiered_candidates, args.role)

        # =========================================================================
        # SUMMARY
        # =========================================================================
        print("\n" + "="*70)
        print("✅ SOURCING AUTOMATION COMPLETE")
        print("="*70)
        print(f"\nResults for: {role_config.get('title', args.role)}")
        print(f"  T1 (Senior): {len(tiered_candidates.get('t1', []))} candidates")
        print(f"  T2 (Mid-level): {len(tiered_candidates.get('t2', []))} candidates")
        print(f"  T3 (Junior): {len(tiered_candidates.get('t3', []))} candidates")
        print(f"  Total: {sum(len(v) for v in tiered_candidates.values())} candidates")

        print(f"\n📁 Output Files:")
        print(f"  1. Raw CSV: {raw_csv_path}")
        print(f"  2. Enriched CSV: {enriched_csv_path}")
        print(f"  3. Final Excel: {excel_path}")

        print(f"\n📋 Next Steps:")
        print(f"  1. Open {os.path.basename(excel_path)}")
        print(f"  2. Review candidates in T1/T2/T3 tabs")
        print(f"  3. Copy DM templates and send via LinkedIn (manually)")
        print(f"  4. Once interest confirmed, add to Markaz via insert_sourced_candidate.py")

        print(f"\n✅ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

        # Log summary
        log_sourcing_action(
            platform="Full Pipeline",
            query=f"{args.role} end-to-end",
            results_found=sum(len(v) for v in tiered_candidates.values()),
            context="pipeline_complete"
        )

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
