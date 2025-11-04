"""
Command-line interface for German Universities scraper.
"""

import argparse
import sys
from .scraper import GermanUniversityScraper


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape and display data for top 10 German universities"
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save data to JSON file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='german_universities.json',
        help='Output filename (default: german_universities.json)'
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Show only summary statistics'
    )

    args = parser.parse_args()

    try:
        scraper = GermanUniversityScraper()

        if args.stats_only:
            stats = scraper.get_summary_statistics()
            print("\n" + "="*80)
            print("GERMAN UNIVERSITIES SUMMARY STATISTICS")
            print("="*80)
            print(f"Total Universities: {stats['total_universities']}")
            print(f"Total Students: {stats['total_students']:,}")
            print(f"Average Students per University: {stats['average_students']:,}")
            print(f"Oldest University: {stats['oldest_university']['name']} ({stats['oldest_university']['founded']})")
            print(f"Newest University: {stats['newest_university']['name']} ({stats['newest_university']['founded']})")
            print(f"Cities: {', '.join(stats['locations'])}")
            print("="*80 + "\n")
        else:
            scraper.print_summary()

        if args.save:
            output_path = scraper.save_to_json(args.output)
            print(f"✓ Data saved to: {output_path}\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
