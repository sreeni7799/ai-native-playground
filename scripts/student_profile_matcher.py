#!/usr/bin/env python3
"""
Student Profile Matcher

Complete student profile matching system that:
1. Takes student preferences and profile
2. Finds matching universities
3. Finds matching scholarships
4. Generates a comprehensive report
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_native_playground.universities.ml_model import UniversityRecommendationModel
from ai_native_playground.scholarships.ml_model import ScholarshipRecommendationModel


class StudentProfileMatcher:
    """Match students with universities and scholarships."""

    def __init__(self):
        """Initialize models."""
        self.uni_model = UniversityRecommendationModel()
        self.scholarship_model = ScholarshipRecommendationModel()

        # Load models
        uni_model_path = Path(__file__).parent.parent / "src" / "ai_native_playground" / "universities" / "data" / "university_recommendation_model_4k.pkl"
        scholarship_model_path = Path(__file__).parent.parent / "src" / "ai_native_playground" / "scholarships" / "data" / "scholarship_recommendation_model.pkl"

        if uni_model_path.exists():
            self.uni_model.load_model(str(uni_model_path))
        else:
            raise FileNotFoundError("University model not found")

        if scholarship_model_path.exists():
            self.scholarship_model.load_model(str(scholarship_model_path))
        else:
            raise FileNotFoundError("Scholarship model not found")

    def create_profile_interactive(self):
        """Create student profile interactively."""
        print("\n" + "="*80)
        print("  🎓 STUDENT PROFILE CREATOR")
        print("="*80 + "\n")

        profile = {}

        # Basic info
        profile['name'] = input("Student name: ").strip()
        profile['field'] = input("Field of study (e.g., Computer Science, Engineering): ").strip()
        profile['country_preference'] = input("Preferred country (or press Enter for any): ").strip() or None
        profile['level'] = input("Education level (Undergraduate/Graduate/PhD): ").strip()

        # Academic info
        try:
            gpa = input("GPA (0-4.0 scale, or press Enter to skip): ").strip()
            profile['gpa'] = float(gpa) if gpa else None
        except ValueError:
            profile['gpa'] = None

        # University preferences
        print("\n--- University Preferences ---")
        uni_type = input("University type (Public/Private, or press Enter for any): ").strip()
        profile['university_type'] = uni_type if uni_type else None

        try:
            max_rank = input("Maximum acceptable ranking (or press Enter for any): ").strip()
            profile['max_rank'] = int(max_rank) if max_rank else None
        except ValueError:
            profile['max_rank'] = None

        try:
            min_students = input("Minimum student population (or press Enter for any): ").strip()
            profile['min_students'] = int(min_students) if min_students else None
        except ValueError:
            profile['min_students'] = None

        # Scholarship preferences
        print("\n--- Scholarship Preferences ---")
        try:
            min_amount = input("Minimum scholarship amount needed ($): ").strip()
            profile['min_scholarship_amount'] = int(min_amount) if min_amount else 0
        except ValueError:
            profile['min_scholarship_amount'] = 0

        renewable = input("Prefer renewable scholarships? (yes/no): ").strip().lower()
        profile['renewable_only'] = renewable in ['yes', 'y']

        scholarship_type = input("Scholarship type (Merit-based/Need-based, or press Enter for any): ").strip()
        profile['scholarship_type'] = scholarship_type if scholarship_type else None

        return profile

    def match_profile(self, profile, n_universities=15, n_scholarships=20):
        """
        Match a student profile with universities and scholarships.

        Args:
            profile: Student profile dictionary
            n_universities: Number of universities to recommend
            n_scholarships: Number of scholarships to recommend

        Returns:
            Dictionary with universities, scholarships, and analysis
        """

        # Build university preferences
        uni_prefs = {}
        if profile.get('country_preference'):
            uni_prefs['country'] = profile['country_preference']
        if profile.get('university_type'):
            uni_prefs['type'] = profile['university_type']
        if profile.get('max_rank'):
            uni_prefs['max_rank'] = profile['max_rank']
        if profile.get('min_students'):
            uni_prefs['min_students'] = profile['min_students']

        # Get university recommendations
        universities = self.uni_model.recommend_by_preferences(
            uni_prefs,
            n_recommendations=n_universities
        )

        # Build scholarship preferences
        scholarship_prefs = {}
        if profile.get('country_preference'):
            scholarship_prefs['country'] = profile['country_preference']
        if profile.get('field'):
            scholarship_prefs['field'] = profile['field']
        if profile.get('level'):
            scholarship_prefs['level'] = profile['level']
        if profile.get('min_scholarship_amount'):
            scholarship_prefs['min_amount'] = profile['min_scholarship_amount']
        if profile.get('renewable_only'):
            scholarship_prefs['renewable'] = True
        if profile.get('scholarship_type'):
            scholarship_prefs['type'] = profile['scholarship_type']

        # Get scholarship recommendations
        scholarships = self.scholarship_model.recommend_by_preferences(
            scholarship_prefs,
            n_recommendations=n_scholarships
        )

        # Categorize universities (reach, match, safety)
        categorized_unis = self._categorize_universities(universities)

        # Calculate statistics
        stats = self._calculate_statistics(universities, scholarships)

        return {
            'profile': profile,
            'universities': universities,
            'categorized_universities': categorized_unis,
            'scholarships': scholarships,
            'statistics': stats
        }

    def _categorize_universities(self, universities):
        """Categorize universities into reach, match, and safety."""
        if not universities:
            return {'reach': [], 'match': [], 'safety': []}

        sorted_unis = sorted(universities, key=lambda x: x['ranking'])

        # Top 30%: Reach schools
        # Middle 40%: Match schools
        # Bottom 30%: Safety schools
        n = len(sorted_unis)
        reach_count = int(n * 0.3)
        match_count = int(n * 0.4)

        return {
            'reach': sorted_unis[:reach_count],
            'match': sorted_unis[reach_count:reach_count + match_count],
            'safety': sorted_unis[reach_count + match_count:]
        }

    def _calculate_statistics(self, universities, scholarships):
        """Calculate statistics for the results."""
        stats = {}

        if universities:
            stats['total_universities'] = len(universities)
            stats['avg_university_ranking'] = sum(u['ranking'] for u in universities) / len(universities)
            stats['avg_student_population'] = sum(u['students'] for u in universities) / len(universities)

            # Countries
            countries = {}
            for u in universities:
                country = u['country']
                countries[country] = countries.get(country, 0) + 1
            stats['university_countries'] = countries

        if scholarships:
            stats['total_scholarships'] = len(scholarships)
            stats['total_funding'] = sum(s['amount'] for s in scholarships)
            stats['avg_scholarship_amount'] = sum(s['amount'] for s in scholarships) / len(scholarships)
            stats['renewable_count'] = sum(1 for s in scholarships if s.get('renewable'))
            stats['renewable_percentage'] = (stats['renewable_count'] / len(scholarships)) * 100

        return stats

    def generate_report(self, results, output_format='text'):
        """
        Generate a comprehensive report.

        Args:
            results: Results from match_profile
            output_format: 'text' or 'markdown'

        Returns:
            Formatted report string
        """

        profile = results['profile']
        universities = results['universities']
        categorized = results['categorized_universities']
        scholarships = results['scholarships']
        stats = results['statistics']

        if output_format == 'markdown':
            return self._generate_markdown_report(profile, universities, categorized, scholarships, stats)
        else:
            return self._generate_text_report(profile, universities, categorized, scholarships, stats)

    def _generate_text_report(self, profile, universities, categorized, scholarships, stats):
        """Generate text report."""
        lines = []
        lines.append("="*80)
        lines.append(f"  STUDENT PROFILE MATCHING REPORT")
        lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*80)
        lines.append("")

        # Profile section
        lines.append("📋 STUDENT PROFILE")
        lines.append("-"*80)
        lines.append(f"Name: {profile.get('name', 'N/A')}")
        lines.append(f"Field of Study: {profile.get('field', 'N/A')}")
        lines.append(f"Education Level: {profile.get('level', 'N/A')}")
        if profile.get('gpa'):
            lines.append(f"GPA: {profile['gpa']}")
        if profile.get('country_preference'):
            lines.append(f"Country Preference: {profile['country_preference']}")
        lines.append("")

        # Statistics
        lines.append("📊 MATCH STATISTICS")
        lines.append("-"*80)
        lines.append(f"Universities Found: {stats.get('total_universities', 0)}")
        lines.append(f"Scholarships Found: {stats.get('total_scholarships', 0)}")
        lines.append(f"Total Potential Funding: ${stats.get('total_funding', 0):,.0f}")
        lines.append(f"Average Scholarship: ${stats.get('avg_scholarship_amount', 0):,.0f}")
        lines.append(f"Renewable Scholarships: {stats.get('renewable_count', 0)} ({stats.get('renewable_percentage', 0):.1f}%)")
        lines.append("")

        # University categories
        if categorized['reach']:
            lines.append("🎯 REACH SCHOOLS (Highly Competitive)")
            lines.append("-"*80)
            for i, uni in enumerate(categorized['reach'], 1):
                lines.append(f"{i}. {uni['name']}")
                lines.append(f"   Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}")
            lines.append("")

        if categorized['match']:
            lines.append("🎓 MATCH SCHOOLS (Good Fit)")
            lines.append("-"*80)
            for i, uni in enumerate(categorized['match'], 1):
                lines.append(f"{i}. {uni['name']}")
                lines.append(f"   Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}")
            lines.append("")

        if categorized['safety']:
            lines.append("✅ SAFETY SCHOOLS (Likely Acceptance)")
            lines.append("-"*80)
            for i, uni in enumerate(categorized['safety'], 1):
                lines.append(f"{i}. {uni['name']}")
                lines.append(f"   Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}")
            lines.append("")

        # Top scholarships
        lines.append("💰 TOP SCHOLARSHIP OPPORTUNITIES")
        lines.append("-"*80)
        for i, s in enumerate(scholarships[:15], 1):
            renewable = " (renewable)" if s.get('renewable') else ""
            lines.append(f"{i}. {s['name']}")
            lines.append(f"   Amount: ${s['amount']:,}{renewable}")
            lines.append(f"   Provider: {s['provider']} | Country: {s['country']}")
            lines.append(f"   Field: {s['field']} | Level: {s['level']}")
            lines.append("")

        lines.append("="*80)
        lines.append("💡 NEXT STEPS")
        lines.append("-"*80)
        lines.append("1. Research each university's specific admission requirements")
        lines.append("2. Verify scholarship eligibility criteria and deadlines")
        lines.append("3. Prepare application materials (essays, recommendations, etc.)")
        lines.append("4. Create an application timeline with all deadlines")
        lines.append("5. Apply to 2-3 reach, 4-6 match, and 2-3 safety schools")
        lines.append("="*80)

        return "\n".join(lines)

    def _generate_markdown_report(self, profile, universities, categorized, scholarships, stats):
        """Generate markdown report."""
        lines = []
        lines.append("# Student Profile Matching Report")
        lines.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Profile
        lines.append("## 📋 Student Profile\n")
        lines.append(f"- **Name**: {profile.get('name', 'N/A')}")
        lines.append(f"- **Field**: {profile.get('field', 'N/A')}")
        lines.append(f"- **Level**: {profile.get('level', 'N/A')}")
        if profile.get('gpa'):
            lines.append(f"- **GPA**: {profile['gpa']}")
        if profile.get('country_preference'):
            lines.append(f"- **Country Preference**: {profile['country_preference']}")
        lines.append("")

        # Stats
        lines.append("## 📊 Match Statistics\n")
        lines.append(f"- **Universities Found**: {stats.get('total_universities', 0)}")
        lines.append(f"- **Scholarships Found**: {stats.get('total_scholarships', 0)}")
        lines.append(f"- **Total Potential Funding**: ${stats.get('total_funding', 0):,.0f}")
        lines.append(f"- **Renewable Scholarships**: {stats.get('renewable_count', 0)} ({stats.get('renewable_percentage', 0):.1f}%)")
        lines.append("")

        # Universities
        if categorized['reach']:
            lines.append("## 🎯 Reach Schools (Highly Competitive)\n")
            for i, uni in enumerate(categorized['reach'], 1):
                lines.append(f"{i}. **{uni['name']}**")
                lines.append(f"   - Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}\n")

        if categorized['match']:
            lines.append("## 🎓 Match Schools (Good Fit)\n")
            for i, uni in enumerate(categorized['match'], 1):
                lines.append(f"{i}. **{uni['name']}**")
                lines.append(f"   - Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}\n")

        if categorized['safety']:
            lines.append("## ✅ Safety Schools (Likely Acceptance)\n")
            for i, uni in enumerate(categorized['safety'], 1):
                lines.append(f"{i}. **{uni['name']}**")
                lines.append(f"   - Ranking: {uni['ranking']} | Students: {uni['students']:,} | Type: {uni['type']}\n")

        # Scholarships
        lines.append("## 💰 Top Scholarship Opportunities\n")
        for i, s in enumerate(scholarships[:15], 1):
            renewable = " (renewable)" if s.get('renewable') else ""
            lines.append(f"{i}. **{s['name']}**")
            lines.append(f"   - Amount: ${s['amount']:,}{renewable}")
            lines.append(f"   - Provider: {s['provider']} | Country: {s['country']}")
            lines.append(f"   - Field: {s['field']} | Level: {s['level']}\n")

        # Next steps
        lines.append("## 💡 Next Steps\n")
        lines.append("1. Research each university's specific admission requirements")
        lines.append("2. Verify scholarship eligibility criteria and deadlines")
        lines.append("3. Prepare application materials")
        lines.append("4. Create application timeline")
        lines.append("5. Apply to 2-3 reach, 4-6 match, 2-3 safety schools")

        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Match student profiles with universities and scholarships")

    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode')
    parser.add_argument('--profile', type=str,
                       help='Path to JSON profile file')
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path')
    parser.add_argument('--format', choices=['text', 'markdown'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--n-universities', type=int, default=15,
                       help='Number of universities (default: 15)')
    parser.add_argument('--n-scholarships', type=int, default=20,
                       help='Number of scholarships (default: 20)')

    args = parser.parse_args()

    try:
        matcher = StudentProfileMatcher()
        print("✓ Models loaded successfully\n")

        # Get profile
        if args.interactive:
            profile = matcher.create_profile_interactive()
        elif args.profile:
            with open(args.profile, 'r') as f:
                profile = json.load(f)
        else:
            print("Error: Use --interactive or --profile <file>")
            return

        # Match profile
        print("\n🔄 Matching profile with universities and scholarships...\n")
        results = matcher.match_profile(profile, args.n_universities, args.n_scholarships)

        # Generate report
        report = matcher.generate_report(results, output_format=args.format)

        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"✅ Report saved to {args.output}")
        else:
            print(report)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure models are trained first.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
