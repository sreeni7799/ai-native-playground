#!/usr/bin/env python3
"""
University + Scholarship Integration Tool

Finds universities matching your criteria and automatically searches for
scholarships available at those universities or in that field/country.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_native_playground.universities.ml_model import UniversityRecommendationModel
from ai_native_playground.scholarships.ml_model import ScholarshipRecommendationModel


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def find_universities_and_scholarships(
    country=None,
    field=None,
    max_rank=None,
    min_rank=None,
    university_type=None,
    min_students=None,
    max_students=None,
    scholarship_min_amount=None,
    scholarship_level="Undergraduate",
    scholarship_renewable=False,
    n_universities=10,
    n_scholarships=10
):
    """
    Find universities and matching scholarships in one go.

    Args:
        country: Target country
        field: Field of study
        max_rank: Maximum university ranking
        min_rank: Minimum university ranking
        university_type: Public or Private
        min_students: Minimum student population
        max_students: Maximum student population
        scholarship_min_amount: Minimum scholarship amount
        scholarship_level: Education level
        scholarship_renewable: Only renewable scholarships
        n_universities: Number of universities to find
        n_scholarships: Number of scholarships to find
    """

    # Load models
    print("🔄 Loading models...")
    uni_model = UniversityRecommendationModel()
    scholarship_model = ScholarshipRecommendationModel()

    # Try to load 4k model first
    uni_model_path = Path(__file__).parent.parent / "src" / "ai_native_playground" / "universities" / "data" / "university_recommendation_model_4k.pkl"
    scholarship_model_path = Path(__file__).parent.parent / "src" / "ai_native_playground" / "scholarships" / "data" / "scholarship_recommendation_model.pkl"

    if uni_model_path.exists():
        uni_model.load_model(str(uni_model_path))
        print(f"✓ Loaded university model ({len(uni_model.universities)} universities)")
    else:
        print("❌ University model not found. Please run generate_4000_data.py first")
        return

    if scholarship_model_path.exists():
        scholarship_model.load_model(str(scholarship_model_path))
        print(f"✓ Loaded scholarship model ({len(scholarship_model.scholarships)} scholarships)")
    else:
        print("❌ Scholarship model not found. Please run generate_scholarships.py first")
        return

    # Build university preferences
    print_header("🎓 UNIVERSITY SEARCH")

    uni_preferences = {}
    if country:
        uni_preferences['country'] = country
    if university_type:
        uni_preferences['type'] = university_type
    if max_rank:
        uni_preferences['max_rank'] = max_rank
    if min_rank:
        uni_preferences['min_rank'] = min_rank
    if min_students:
        uni_preferences['min_students'] = min_students
    if max_students:
        uni_preferences['max_students'] = max_students

    print("Search Criteria:")
    for key, value in uni_preferences.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    print()

    # Get university recommendations
    universities = uni_model.recommend_by_preferences(
        uni_preferences,
        n_recommendations=n_universities
    )

    if not universities:
        print("❌ No universities found matching criteria.")
        return

    print(f"Found {len(universities)} universities:\n")

    for i, uni in enumerate(universities, 1):
        print(f"{i}. {uni['name']}")
        city = uni.get('city', uni.get('location', 'N/A'))
        country = uni.get('country', 'N/A')
        print(f"   📍 {city}, {country}")
        print(f"   📊 Ranking: {uni['ranking']} | Students: {uni['students']:,}")
        print(f"   🏛  Type: {uni['type']} | Founded: {uni['founded']}")
        print()

    # Build scholarship preferences
    print_header("💰 SCHOLARSHIP SEARCH")

    scholarship_preferences = {}
    if country:
        scholarship_preferences['country'] = country
    if field:
        scholarship_preferences['field'] = field
    if scholarship_level:
        scholarship_preferences['level'] = scholarship_level
    if scholarship_min_amount:
        scholarship_preferences['min_amount'] = scholarship_min_amount
    if scholarship_renewable:
        scholarship_preferences['renewable'] = True

    print("Search Criteria:")
    for key, value in scholarship_preferences.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    print()

    # Get scholarship recommendations
    scholarships = scholarship_model.recommend_by_preferences(
        scholarship_preferences,
        n_recommendations=n_scholarships
    )

    if not scholarships:
        print("❌ No scholarships found matching criteria.")
        return

    print(f"Found {len(scholarships)} scholarships:\n")

    for i, s in enumerate(scholarships, 1):
        renewable_text = " (renewable annually)" if s.get('renewable') else " (one-time)"
        print(f"{i}. {s['name']}")
        print(f"   💰 Amount: ${s['amount']:,}{renewable_text}")
        print(f"   🏛  Provider: {s['provider']}")
        print(f"   🌍 Country: {s['country']}")
        print(f"   📚 Field: {s['field']} | Level: {s['level']}")
        print(f"   📋 Type: {s['type']}")
        print()

    # Summary
    print_header("📊 SUMMARY")

    total_scholarship_value = sum(s['amount'] for s in scholarships)
    renewable_count = sum(1 for s in scholarships if s.get('renewable'))

    print(f"Universities Found: {len(universities)}")
    print(f"Scholarships Found: {len(scholarships)}")
    print(f"Total Potential Funding: ${total_scholarship_value:,}")
    print(f"Renewable Scholarships: {renewable_count} ({renewable_count/len(scholarships)*100:.1f}%)")
    print()

    # Calculate avg per university
    avg_ranking = sum(u['ranking'] for u in universities) / len(universities)
    print(f"Average University Ranking: {avg_ranking:.1f}")
    print(f"Average Scholarship Amount: ${total_scholarship_value / len(scholarships):,.0f}")
    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Find universities and matching scholarships in one search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find top CS schools and scholarships
  python university_scholarship_finder.py --country "United States" \\
    --field "Computer Science" --max-rank 50 --scholarship-min-amount 20000

  # Find engineering programs with high scholarships
  python university_scholarship_finder.py --field Engineering \\
    --max-rank 100 --scholarship-min-amount 30000 --scholarship-renewable

  # International student search
  python university_scholarship_finder.py --country Canada \\
    --scholarship-level Graduate --n-universities 20 --n-scholarships 20
        """
    )

    # University filters
    parser.add_argument('--country', '-c', type=str, help='Country name')
    parser.add_argument('--field', '-f', type=str, help='Field of study')
    parser.add_argument('--max-rank', type=int, help='Maximum university ranking')
    parser.add_argument('--min-rank', type=int, help='Minimum university ranking')
    parser.add_argument('--type', type=str, help='University type (Public/Private)')
    parser.add_argument('--min-students', type=int, help='Minimum student population')
    parser.add_argument('--max-students', type=int, help='Maximum student population')

    # Scholarship filters
    parser.add_argument('--scholarship-min-amount', type=int, help='Minimum scholarship amount')
    parser.add_argument('--scholarship-level', type=str, default='Undergraduate',
                       help='Education level (default: Undergraduate)')
    parser.add_argument('--scholarship-renewable', action='store_true',
                       help='Only renewable scholarships')

    # Results
    parser.add_argument('--n-universities', type=int, default=10,
                       help='Number of universities to find (default: 10)')
    parser.add_argument('--n-scholarships', type=int, default=10,
                       help='Number of scholarships to find (default: 10)')

    args = parser.parse_args()

    # Run search
    find_universities_and_scholarships(
        country=args.country,
        field=args.field,
        max_rank=args.max_rank,
        min_rank=args.min_rank,
        university_type=args.type,
        min_students=args.min_students,
        max_students=args.max_students,
        scholarship_min_amount=args.scholarship_min_amount,
        scholarship_level=args.scholarship_level,
        scholarship_renewable=args.scholarship_renewable,
        n_universities=args.n_universities,
        n_scholarships=args.n_scholarships
    )


if __name__ == '__main__':
    main()
