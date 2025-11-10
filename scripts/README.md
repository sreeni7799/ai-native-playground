# 🔧 Integration Scripts

Powerful scripts that combine multiple AI Native Playground tools for common workflows.

## Available Scripts

### 1. University + Scholarship Finder
**File**: `university_scholarship_finder.py`

Find universities and matching scholarships in a single search.

**Usage**:
```bash
# Make executable
chmod +x university_scholarship_finder.py

# Find CS schools and scholarships
python university_scholarship_finder.py \
  --country "United States" \
  --field "Computer Science" \
  --max-rank 50 \
  --scholarship-min-amount 20000

# Engineering programs with high scholarships
python university_scholarship_finder.py \
  --field Engineering \
  --max-rank 100 \
  --scholarship-min-amount 30000 \
  --scholarship-renewable

# International student search
python university_scholarship_finder.py \
  --country Canada \
  --scholarship-level Graduate \
  --n-universities 20 \
  --n-scholarships 20
```

**Options**:
- `--country`: Target country
- `--field`: Field of study
- `--max-rank`: Maximum university ranking
- `--min-rank`: Minimum university ranking
- `--type`: University type (Public/Private)
- `--min-students`: Minimum student population
- `--max-students`: Maximum student population
- `--scholarship-min-amount`: Minimum scholarship amount
- `--scholarship-level`: Education level
- `--scholarship-renewable`: Only renewable scholarships
- `--n-universities`: Number of universities (default: 10)
- `--n-scholarships`: Number of scholarships (default: 10)

---

### 2. Student Profile Matcher
**File**: `student_profile_matcher.py`

Complete student profile matching with universities and scholarships, generates comprehensive reports.

**Usage**:

**Interactive Mode**:
```bash
chmod +x student_profile_matcher.py
python student_profile_matcher.py --interactive
# Answer questions to build your profile
```

**From JSON Profile**:
```bash
# Create a profile file
cat > my_profile.json << EOF
{
  "name": "Sarah Johnson",
  "field": "Computer Science",
  "level": "Undergraduate",
  "country_preference": "United States",
  "gpa": 3.8,
  "university_type": "Private",
  "max_rank": 50,
  "min_scholarship_amount": 20000,
  "renewable_only": true
}
EOF

# Generate report
python student_profile_matcher.py \
  --profile my_profile.json \
  --output report.txt \
  --n-universities 15 \
  --n-scholarships 20

# Generate markdown report
python student_profile_matcher.py \
  --profile my_profile.json \
  --output report.md \
  --format markdown
```

**Features**:
- Categorizes universities into Reach, Match, and Safety schools
- Finds matching scholarships based on profile
- Calculates comprehensive statistics
- Generates professional reports in text or markdown format
- Includes next steps and recommendations

**Options**:
- `--interactive`, `-i`: Interactive mode
- `--profile`: Path to JSON profile file
- `--output`, `-o`: Output file path
- `--format`: Output format (text or markdown)
- `--n-universities`: Number of universities (default: 15)
- `--n-scholarships`: Number of scholarships (default: 20)

---

### 3. Daily Digest
**File**: `daily_digest.sh`

Automated daily summary combining weather, news, tasks, and optional scholarship/university updates.

**Usage**:
```bash
# Make executable
chmod +x daily_digest.sh

# Basic usage (defaults to Boston)
./daily_digest.sh

# Specify city
./daily_digest.sh London

# Specify city and country
./daily_digest.sh Toronto Canada

# Include scholarship updates
./daily_digest.sh Boston "United States" --scholarships

# Include university info
./daily_digest.sh Boston "United States" --universities
```

**What it includes**:
- 🌤️ Weather forecast for your city
- 📰 Top 5 tech news headlines
- ✅ Your daily task list
- 💰 Optional: New scholarship opportunities
- 🎓 Optional: University information
- 📊 Quick stats (date, time, system info)
- 💡 Daily reminders

**Automate with Cron**:
```bash
# Edit crontab
crontab -e

# Add line to run daily at 8 AM
0 8 * * * /path/to/scripts/daily_digest.sh Boston "United States" > ~/daily_digest.log 2>&1

# Run with scholarships every Monday
0 8 * * 1 /path/to/scripts/daily_digest.sh Boston "United States" --scholarships
```

**Requirements**:
- Weather API must be running (`weather-api`) for weather updates
- Other tools auto-detected and skipped if unavailable

---

## Installation

### Prerequisites
```bash
# Install the main package first
cd /path/to/ai-native-playground
pip install -e .

# Make scripts executable
chmod +x scripts/*.py scripts/*.sh
```

### Generate Required Data
```bash
# Generate university data (if not already done)
python -m ai_native_playground.universities.generate_4000_data

# Generate scholarship data (if not already done)
python -m ai_native_playground.scholarships.generate_scholarships
```

---

## Example Workflows

### Workflow 1: Complete University Search for a Student

```bash
# Step 1: Create student profile
python scripts/student_profile_matcher.py --interactive

# Step 2: Get detailed university + scholarship matches
python scripts/university_scholarship_finder.py \
  --country "United States" \
  --field "Engineering" \
  --max-rank 100 \
  --scholarship-min-amount 25000 \
  --scholarship-renewable \
  --n-universities 20 \
  --n-scholarships 30 > detailed_search.txt

# Step 3: Add application deadlines to tasks
todo-app add "Stanford application - Nov 1"
todo-app add "MIT application - Nov 1"
todo-app add "Apply for NSF Fellowship - Oct 15"

# Step 4: Set up daily digest
./scripts/daily_digest.sh --scholarships
```

### Workflow 2: Education Consultant Managing Multiple Clients

```bash
# Create profile for each client
mkdir -p client_profiles
mkdir -p client_reports

# Client 1: Sarah (CS major)
cat > client_profiles/sarah.json << EOF
{
  "name": "Sarah Johnson",
  "field": "Computer Science",
  "level": "Undergraduate",
  "country_preference": "United States",
  "gpa": 3.9,
  "max_rank": 30,
  "min_scholarship_amount": 30000
}
EOF

# Client 2: Alex (Engineering)
cat > client_profiles/alex.json << EOF
{
  "name": "Alex Chen",
  "field": "Engineering",
  "level": "Graduate",
  "country_preference": "Canada",
  "min_scholarship_amount": 25000,
  "renewable_only": true
}
EOF

# Generate reports for all clients
for profile in client_profiles/*.json; do
    name=$(basename "$profile" .json)
    echo "Processing $name..."

    python scripts/student_profile_matcher.py \
        --profile "$profile" \
        --output "client_reports/${name}_report.md" \
        --format markdown \
        --n-universities 20 \
        --n-scholarships 25

    echo "✅ Report generated: client_reports/${name}_report.md"
done

echo "All client reports generated!"
```

### Workflow 3: Research Project - Batch Data Collection

```bash
# Collect data for multiple countries
COUNTRIES=("United States" "United Kingdom" "Canada" "Germany" "Australia")

for country in "${COUNTRIES[@]}"; do
    echo "Collecting data for $country..."

    # Universities
    universities --country "$country" --export "data/${country// /_}_universities.json"

    # Scholarships
    scholarship-recommend --country "$country" --n 50 > "data/${country// /_}_scholarships.txt"

    # Combined search
    python scripts/university_scholarship_finder.py \
        --country "$country" \
        --n-universities 30 \
        --n-scholarships 50 > "data/${country// /_}_combined.txt"
done

echo "Data collection complete!"
```

---

## Advanced Usage

### Combining with Other Tools

**1. Send Daily Digest via Email**:
```bash
./scripts/daily_digest.sh Boston "United States" --scholarships | \
    mail -s "Your Daily Digest - $(date +%Y-%m-%d)" your@email.com
```

**2. Export to PDF** (requires `wkhtmltopdf`):
```bash
python scripts/student_profile_matcher.py \
    --profile my_profile.json \
    --format markdown \
    --output report.md

# Convert to PDF
pandoc report.md -o report.pdf
```

**3. Integration with Discord/Slack**:
```bash
# Send scholarship alerts to Discord webhook
SCHOLARSHIPS=$(python scripts/university_scholarship_finder.py \
    --field "Computer Science" \
    --scholarship-min-amount 40000 \
    --n-scholarships 5)

curl -X POST YOUR_DISCORD_WEBHOOK_URL \
    -H "Content-Type: application/json" \
    -d "{\"content\":\"New Scholarships Found:\n\`\`\`$SCHOLARSHIPS\`\`\`\"}"
```

---

## Troubleshooting

**Problem**: `ModuleNotFoundError` when running scripts
```bash
# Solution: Install package in development mode
pip install -e .
```

**Problem**: "Model not found" errors
```bash
# Solution: Generate the data first
python -m ai_native_playground.universities.generate_4000_data
python -m ai_native_playground.scholarships.generate_scholarships
```

**Problem**: Weather not showing in daily digest
```bash
# Solution: Start the weather API server
weather-api &
# Or in a separate terminal
weather-api
```

**Problem**: Script permissions denied
```bash
# Solution: Make scripts executable
chmod +x scripts/*.py scripts/*.sh
```

---

## Creating Custom Scripts

You can create your own integration scripts! Here's a template:

```python
#!/usr/bin/env python3
"""
Custom Integration Script Template
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import modules
from ai_native_playground.universities.ml_model import UniversityRecommendationModel
from ai_native_playground.scholarships.ml_model import ScholarshipRecommendationModel

def main():
    # Your custom logic here
    pass

if __name__ == '__main__':
    main()
```

---

## Contributing

Have an idea for a new integration script?

1. Create your script in the `scripts/` directory
2. Add documentation to this README
3. Test thoroughly
4. Submit a pull request!

---

## Support

For issues or questions:
- Check the main [README](../README.md)
- See [EXAMPLES.md](../EXAMPLES.md) for more use cases
- See [QUICKSTART.md](../QUICKSTART.md) for getting started

---

**Happy automating! 🚀**
