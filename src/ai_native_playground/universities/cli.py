"""
Command-line interface for University Dataset.
Access and analyze data for 1000+ universities across US, Canada, Germany, UK, Australia, and France.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any


class UniversityCLI:
    """CLI for university dataset operations."""

    def __init__(self):
        """Initialize the CLI."""
        self.data_path = Path(__file__).parent / "data" / "universities_1000_dataset.json"
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load the university dataset."""
        if not self.data_path.exists():
            print(f"Error: Dataset not found at {self.data_path}")
            print("Please run: python -m ai_native_playground.universities.generate_data")
            sys.exit(1)

        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_universities(self, country: Optional[str] = None, limit: int = 10):
        """List universities with optional country filter."""
        if country:
            country_key = country.lower().replace(" ", "_")
            if country_key not in self.data:
                print(f"Error: Country '{country}' not found.")
                print(f"Available countries: {', '.join(self.data.keys())}")
                return

            unis = self.data[country_key]
            print(f"\n{'='*80}")
            print(f"{country.upper()} UNIVERSITIES ({len(unis)} total)")
            print(f"{'='*80}\n")

            for i, uni in enumerate(unis[:limit], 1):
                self._print_university(uni, i)

            if len(unis) > limit:
                print(f"\n... and {len(unis) - limit} more universities")

        else:
            # List from all countries
            print(f"\n{'='*80}")
            print(f"GLOBAL UNIVERSITY DATASET")
            print(f"{'='*80}\n")

            for country_name, unis in self.data.items():
                print(f"{country_name.replace('_', ' ').title()}: {len(unis)} universities")

            print(f"\nTotal: {sum(len(unis) for unis in self.data.values())} universities")

    def _print_university(self, uni: Dict[str, Any], index: int):
        """Print formatted university information."""
        print(f"{index}. {uni['name']}")

        # Location
        if 'state' in uni:
            print(f"   Location: {uni['city']}, {uni['state']}")
        elif 'province' in uni:
            print(f"   Location: {uni['city']}, {uni['province']}")
        elif 'region' in uni:
            print(f"   Location: {uni['city']}, {uni['region']}")
        else:
            print(f"   Location: {uni.get('city', 'N/A')}")

        print(f"   Founded: {uni['founded']}")
        print(f"   Type: {uni['type']}")
        print(f"   Students: {uni['students']:,}")
        print(f"   World Ranking: #{uni['ranking']}")

        if 'notable_programs' in uni:
            print(f"   Notable Programs: {', '.join(uni['notable_programs'])}")

        print()

    def show_statistics(self):
        """Show comprehensive statistics about the dataset."""
        print(f"\n{'='*80}")
        print("UNIVERSITY DATASET STATISTICS")
        print(f"{'='*80}\n")

        total_universities = sum(len(unis) for unis in self.data.values())
        total_students = sum(uni['students'] for unis in self.data.values() for uni in unis)

        print(f"Total Universities: {total_universities}")
        print(f"Total Students: {total_students:,}")
        print(f"Average Students per University: {total_students // total_universities:,}\n")

        print("Universities by Country:")
        for country_name, unis in self.data.items():
            country_display = country_name.replace('_', ' ').title()
            country_students = sum(uni['students'] for uni in unis)
            print(f"  {country_display:25s}: {len(unis):3d} universities, {country_students:,} students")

        # Find extremes
        all_unis_with_country = []
        for country, unis in self.data.items():
            for uni in unis:
                uni_copy = uni.copy()
                uni_copy['country'] = country.replace('_', ' ').title()
                all_unis_with_country.append(uni_copy)

        oldest = min(all_unis_with_country, key=lambda x: x['founded'])
        newest = max(all_unis_with_country, key=lambda x: x['founded'])
        largest = max(all_unis_with_country, key=lambda x: x['students'])
        smallest = min(all_unis_with_country, key=lambda x: x['students'])
        top_ranked = min(all_unis_with_country, key=lambda x: x['ranking'])

        print(f"\nDataset Highlights:")
        print(f"  Oldest University: {oldest['name']} ({oldest['founded']}, {oldest['country']})")
        print(f"  Newest University: {newest['name']} ({newest['founded']}, {newest['country']})")
        print(f"  Largest University: {largest['name']} ({largest['students']:,} students, {largest['country']})")
        print(f"  Smallest University: {smallest['name']} ({smallest['students']:,} students, {smallest['country']})")
        print(f"  Top Ranked: {top_ranked['name']} (#{top_ranked['ranking']}, {top_ranked['country']})")
        print(f"{'='*80}\n")

    def search_universities(self, query: str, country: Optional[str] = None):
        """Search universities by name."""
        query = query.lower()
        results = []

        data_to_search = self.data
        if country:
            country_key = country.lower().replace(" ", "_")
            if country_key in self.data:
                data_to_search = {country_key: self.data[country_key]}
            else:
                print(f"Error: Country '{country}' not found.")
                return

        for country_name, unis in data_to_search.items():
            for uni in unis:
                if query in uni['name'].lower() or query in uni.get('city', '').lower():
                    uni_copy = uni.copy()
                    uni_copy['country'] = country_name.replace('_', ' ').title()
                    results.append(uni_copy)

        if results:
            print(f"\n{'='*80}")
            print(f"SEARCH RESULTS: '{query}' ({len(results)} matches)")
            print(f"{'='*80}\n")

            for i, uni in enumerate(results, 1):
                self._print_university(uni, i)
        else:
            print(f"\nNo universities found matching '{query}'")

    def export_data(self, country: Optional[str] = None, output: str = "universities_export.json"):
        """Export university data to a file."""
        if country:
            country_key = country.lower().replace(" ", "_")
            if country_key not in self.data:
                print(f"Error: Country '{country}' not found.")
                return

            export_data = {country_key: self.data[country_key]}
        else:
            export_data = self.data

        output_path = Path(output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        total_unis = sum(len(unis) for unis in export_data.values())
        print(f"✓ Exported {total_unis} universities to: {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Access and analyze data for 1000+ universities worldwide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show statistics
  universities --stats

  # List all US universities
  universities --country "United States" --limit 20

  # Search for universities
  universities --search "Stanford"

  # Export data for a specific country
  universities --country Germany --export german_unis.json
        """
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List universities'
    )
    parser.add_argument(
        '--country',
        type=str,
        help='Filter by country (United States, Canada, Germany, United Kingdom, Australia, France)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of universities to display (default: 10)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show dataset statistics'
    )
    parser.add_argument(
        '--search',
        type=str,
        help='Search universities by name or city'
    )
    parser.add_argument(
        '--export',
        type=str,
        metavar='FILE',
        help='Export data to JSON file'
    )

    args = parser.parse_args()

    try:
        cli = UniversityCLI()

        if args.stats:
            cli.show_statistics()
        elif args.search:
            cli.search_universities(args.search, args.country)
        elif args.export:
            cli.export_data(args.country, args.export)
        elif args.list or args.country:
            cli.list_universities(args.country, args.limit)
        else:
            # Default: show statistics
            cli.show_statistics()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
