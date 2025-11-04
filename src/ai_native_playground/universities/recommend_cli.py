"""
CLI for University Recommendation System

Use the trained ML model to get personalized university recommendations.
"""

import argparse
import sys
from pathlib import Path
from .ml_model import UniversityRecommendationModel


class RecommendationCLI:
    """CLI interface for university recommendations."""

    def __init__(self):
        """Initialize the CLI with trained model."""
        self.model_path = Path(__file__).parent / "data" / "university_recommendation_model.pkl"
        self.model = UniversityRecommendationModel()

        if self.model_path.exists():
            self.model.load_model(str(self.model_path))
        else:
            print(f"Error: Trained model not found at {self.model_path}")
            print("Please train the model first:")
            print("  python -m ai_native_playground.universities.ml_model")
            sys.exit(1)

    def recommend_similar(self, university_name: str, n_recommendations: int = 5):
        """Show universities similar to a given university."""
        recommendations = self.model.recommend_similar(university_name, n_recommendations)

        if not recommendations:
            print(f"\n❌ University '{university_name}' not found.")
            print("Try searching for a different university name.")
            return

        print(f"\n{'='*80}")
        print(f"UNIVERSITIES SIMILAR TO: {university_name.upper()}")
        print(f"{'='*80}\n")

        for i, uni in enumerate(recommendations, 1):
            self._print_university(uni, i, show_similarity=True)

    def recommend_by_preferences(self, preferences: dict, n_recommendations: int = 10):
        """Show recommendations based on preferences."""
        recommendations = self.model.recommend_by_preferences(preferences, n_recommendations)

        if not recommendations:
            print("\n❌ No universities match your criteria.")
            print("Try adjusting your preferences.")
            return

        print(f"\n{'='*80}")
        print("RECOMMENDED UNIVERSITIES BASED ON YOUR PREFERENCES")
        print(f"{'='*80}")
        print(f"Filters applied: {self._format_preferences(preferences)}")
        print(f"Found {len(recommendations)} matching universities\n")

        for i, uni in enumerate(recommendations, 1):
            self._print_university(uni, i)

    def _print_university(self, uni: dict, index: int, show_similarity: bool = False):
        """Print formatted university information."""
        print(f"{index}. {uni['name']}")

        # Location
        if 'state' in uni:
            print(f"   Location: {uni['city']}, {uni['state']}, USA")
        elif 'province' in uni:
            print(f"   Location: {uni['city']}, {uni['province']}, Canada")
        elif 'region' in uni:
            print(f"   Location: {uni['city']}, {uni['region']}, UK")
        else:
            print(f"   Location: {uni.get('city', 'N/A')}")

        print(f"   Founded: {uni['founded']}")
        print(f"   Type: {uni['type']}")
        print(f"   Students: {uni['students']:,}")
        print(f"   World Ranking: #{uni['ranking']}")

        if show_similarity and 'similarity_score' in uni:
            print(f"   Similarity Score: {uni['similarity_score']:.2%}")

        print()

    def _format_preferences(self, prefs: dict) -> str:
        """Format preferences for display."""
        parts = []
        if 'country' in prefs:
            parts.append(f"Country: {prefs['country']}")
        if 'max_ranking' in prefs:
            parts.append(f"Ranking ≤ {prefs['max_ranking']}")
        if 'min_students' in prefs:
            parts.append(f"Students ≥ {prefs['min_students']:,}")
        if 'max_students' in prefs:
            parts.append(f"Students ≤ {prefs['max_students']:,}")
        if 'university_type' in prefs:
            parts.append(f"Type: {prefs['university_type']}")

        return ", ".join(parts) if parts else "None"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Get personalized university recommendations using ML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find universities similar to Stanford
  university-recommend --similar "Stanford University"

  # Get recommendations for top-ranked universities in the US
  university-recommend --country "United States" --max-rank 50

  # Find large public universities
  university-recommend --type Public --min-students 30000 --limit 10

  # Find small private universities with good rankings
  university-recommend --type Private --max-students 15000 --max-rank 100
        """
    )

    # Similar universities
    parser.add_argument(
        '--similar',
        type=str,
        metavar='NAME',
        help='Find universities similar to this one'
    )

    # Preference-based recommendations
    parser.add_argument(
        '--country',
        type=str,
        help='Filter by country (e.g., "United States", "Canada", "Germany")'
    )
    parser.add_argument(
        '--max-rank',
        type=int,
        metavar='N',
        help='Maximum ranking (e.g., 100 for top 100)'
    )
    parser.add_argument(
        '--min-rank',
        type=int,
        metavar='N',
        help='Minimum ranking'
    )
    parser.add_argument(
        '--min-students',
        type=int,
        metavar='N',
        help='Minimum number of students'
    )
    parser.add_argument(
        '--max-students',
        type=int,
        metavar='N',
        help='Maximum number of students'
    )
    parser.add_argument(
        '--type',
        type=str,
        choices=['Public', 'Private'],
        help='University type'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Number of recommendations (default: 10)'
    )

    args = parser.parse_args()

    try:
        cli = RecommendationCLI()

        if args.similar:
            # Find similar universities
            cli.recommend_similar(args.similar, n_recommendations=args.limit)

        else:
            # Build preferences from arguments
            preferences = {}

            if args.country:
                preferences['country'] = args.country
            if args.max_rank:
                preferences['max_ranking'] = args.max_rank
            if args.min_rank:
                preferences['min_ranking'] = args.min_rank
            if args.min_students:
                preferences['min_students'] = args.min_students
            if args.max_students:
                preferences['max_students'] = args.max_students
            if args.type:
                preferences['university_type'] = args.type

            if preferences:
                cli.recommend_by_preferences(preferences, n_recommendations=args.limit)
            else:
                parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
