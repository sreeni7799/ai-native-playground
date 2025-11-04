"""
CLI for Scholarship Recommendations using ML Model

Uses trained ML model to recommend scholarships based on preferences.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any
from .ml_model import ScholarshipRecommendationModel


class ScholarshipRecommender:
    """CLI wrapper for scholarship recommendations."""

    def __init__(self):
        """Initialize the recommender."""
        self.model_path = Path(__file__).parent / "data" / "scholarship_recommendation_model.pkl"
        self.model = ScholarshipRecommendationModel()

        # Load model if it exists
        if self.model_path.exists():
            self.model.load_model(str(self.model_path))
        else:
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Please run: python -m ai_native_playground.scholarships.generate_scholarships"
            )

    def recommend_interactive(self):
        """Interactive recommendation mode."""
        print("\n" + "="*80)
        print("💰 SCHOLARSHIP RECOMMENDATION SYSTEM - ML Powered")
        print("="*80)
        print(f"\n✓ Loaded trained model with {len(self.model.scholarships):,} scholarships")
        print("\nAnswer the following questions to get personalized recommendations:")
        print("(Press Enter to skip any question)\n")

        preferences = {}

        # Country
        country = input("Preferred country (e.g., United States, UK, Germany): ").strip()
        if country:
            preferences['country'] = country

        # Field of study
        field = input("Field of study (e.g., Engineering, Computer Science, Medicine): ").strip()
        if field:
            preferences['field'] = field

        # Level
        level = input("Education level (Undergraduate/Graduate/Doctoral): ").strip()
        if level:
            preferences['level'] = level

        # Type
        scholarship_type = input("Scholarship type (Merit-based/Need-based/Athletic/Research): ").strip()
        if scholarship_type:
            preferences['type'] = scholarship_type

        # Amount range
        min_amount = input("Minimum scholarship amount (e.g., 10000): ").strip()
        if min_amount:
            try:
                preferences['min_amount'] = int(min_amount)
            except ValueError:
                print("Invalid amount, skipping...")

        max_amount = input("Maximum scholarship amount (e.g., 50000): ").strip()
        if max_amount:
            try:
                preferences['max_amount'] = int(max_amount)
            except ValueError:
                print("Invalid amount, skipping...")

        # Renewable
        renewable = input("Only renewable scholarships? (yes/no): ").strip().lower()
        if renewable in ['yes', 'y']:
            preferences['renewable'] = True
        elif renewable in ['no', 'n']:
            preferences['renewable'] = False

        # Get number of recommendations
        n_recs = input("\nHow many recommendations? (default: 10): ").strip()
        try:
            n_recs = int(n_recs) if n_recs else 10
        except ValueError:
            n_recs = 10

        # Get recommendations
        print("\n" + "="*80)
        print("SCHOLARSHIP RECOMMENDATIONS")
        print("="*80 + "\n")

        if not preferences:
            print("No preferences specified. Showing top scholarships by amount...\n")
            preferences = {}

        recommendations = self.model.recommend_by_preferences(
            preferences,
            n_recommendations=n_recs
        )

        if not recommendations:
            print("❌ No scholarships found matching your criteria.")
            print("Try broadening your search parameters.")
            return

        self._display_recommendations(recommendations, preferences)

    def recommend_by_args(self, args):
        """Recommend based on command-line arguments."""
        preferences = {}

        if args.country:
            preferences['country'] = args.country
        if args.field:
            preferences['field'] = args.field
        if args.level:
            preferences['level'] = args.level
        if args.type:
            preferences['type'] = args.type
        if args.min_amount:
            preferences['min_amount'] = args.min_amount
        if args.max_amount:
            preferences['max_amount'] = args.max_amount
        if args.renewable:
            preferences['renewable'] = True

        recommendations = self.model.recommend_by_preferences(
            preferences,
            n_recommendations=args.n
        )

        print("\n" + "="*80)
        print("SCHOLARSHIP RECOMMENDATIONS")
        print("="*80 + "\n")

        if not recommendations:
            print("❌ No scholarships found matching your criteria.")
            return

        self._display_recommendations(recommendations, preferences)

    def find_similar_scholarships(self, scholarship_name: str, n: int = 5):
        """Find scholarships similar to a given scholarship."""
        print("\n" + "="*80)
        print(f"SCHOLARSHIPS SIMILAR TO: {scholarship_name}")
        print("="*80 + "\n")

        similar = self.model.find_similar(scholarship_name, n_recommendations=n)

        if not similar:
            print(f"❌ Scholarship '{scholarship_name}' not found.")
            print("Try a different name or partial match.")
            return

        for i, s in enumerate(similar, 1):
            renewable_text = " (renewable)" if s.get('renewable') else ""
            similarity = s.get('similarity_score', 0)

            print(f"{i}. {s['name']}")
            print(f"   Amount: ${s['amount']:,}{renewable_text}")
            print(f"   Provider: {s['provider']}")
            print(f"   Country: {s['country']}")
            print(f"   Field: {s['field']} | Level: {s['level']}")
            print(f"   Type: {s['type']}")
            print(f"   Similarity Score: {similarity:.3f}")
            print()

    def _display_recommendations(
        self,
        recommendations: list,
        preferences: Dict[str, Any]
    ):
        """Display scholarship recommendations."""
        print(f"Found {len(recommendations)} scholarships matching your criteria:\n")

        if preferences:
            print("Search Criteria:")
            for key, value in preferences.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
            print()

        for i, s in enumerate(recommendations, 1):
            renewable_text = " (renewable annually)" if s.get('renewable') else " (one-time)"
            deadline = s.get('deadline', 'Rolling')
            fee = s.get('application_fee', 0)
            fee_text = f"${fee}" if fee > 0 else "No fee"

            print(f"{i}. {s['name']}")
            print(f"   💰 Amount: ${s['amount']:,}{renewable_text}")
            print(f"   🏛  Provider: {s['provider']}")
            print(f"   🌍 Country: {s['country']}")
            print(f"   📚 Field: {s['field']} | 🎓 Level: {s['level']}")
            print(f"   📋 Type: {s['type']}")
            print(f"   📅 Deadline: {deadline} | 💳 Fee: {fee_text}")

            if s.get('description'):
                desc = s['description']
                if len(desc) > 100:
                    desc = desc[:97] + "..."
                print(f"   📝 {desc}")

            print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Get ML-powered scholarship recommendations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  scholarship-recommend

  # Recommend engineering scholarships in US
  scholarship-recommend --country "United States" --field Engineering

  # High-value graduate scholarships
  scholarship-recommend --level Graduate --min-amount 30000

  # Renewable scholarships
  scholarship-recommend --renewable --min-amount 20000

  # Find similar scholarships
  scholarship-recommend --similar "Fulbright"
        """
    )

    parser.add_argument(
        '--country', '-c',
        type=str,
        help='Preferred country'
    )
    parser.add_argument(
        '--field', '-f',
        type=str,
        help='Field of study'
    )
    parser.add_argument(
        '--level', '-l',
        type=str,
        help='Education level (Undergraduate/Graduate/Doctoral)'
    )
    parser.add_argument(
        '--type', '-t',
        type=str,
        help='Scholarship type (Merit-based/Need-based/etc.)'
    )
    parser.add_argument(
        '--min-amount',
        type=int,
        help='Minimum scholarship amount'
    )
    parser.add_argument(
        '--max-amount',
        type=int,
        help='Maximum scholarship amount'
    )
    parser.add_argument(
        '--renewable',
        action='store_true',
        help='Only show renewable scholarships'
    )
    parser.add_argument(
        '--n',
        type=int,
        default=10,
        help='Number of recommendations (default: 10)'
    )
    parser.add_argument(
        '--similar',
        type=str,
        help='Find scholarships similar to this one'
    )

    args = parser.parse_args()

    try:
        recommender = ScholarshipRecommender()

        if args.similar:
            # Find similar scholarships
            recommender.find_similar_scholarships(args.similar, n=args.n)
        elif any([args.country, args.field, args.level, args.type,
                  args.min_amount, args.max_amount, args.renewable]):
            # Use command-line arguments
            recommender.recommend_by_args(args)
        else:
            # Interactive mode
            recommender.recommend_interactive()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
