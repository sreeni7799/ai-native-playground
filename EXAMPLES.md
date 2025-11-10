# 📚 Real-World Examples & Use Cases

Practical examples showing how to use AI Native Playground for real scenarios.

## Table of Contents
- [Student Examples](#student-examples)
- [Developer Examples](#developer-examples)
- [Researcher Examples](#researcher-examples)
- [Professional Examples](#professional-examples)
- [Advanced Workflows](#advanced-workflows)

---

## Student Examples

### Example 1: High School Senior Planning College Applications

**Background**: Sarah is a high school senior interested in Computer Science. She wants to apply to 10-15 schools and needs scholarships.

#### Step 1: Build University List (Reach, Match, Safety)

```bash
# Reach schools (top 20)
university-recommend --max-rank 20 --limit 10
# Output: MIT, Stanford, Carnegie Mellon, UC Berkeley, etc.

# Match schools (ranked 20-50)
university-recommend --min-rank 20 --max-rank 50 --limit 10
# Output: Georgia Tech, UT Austin, University of Washington, etc.

# Safety schools (ranked 50-100)
university-recommend --min-rank 50 --max-rank 100 --type Public --limit 10
# Output: Penn State, Ohio State, Purdue, etc.
```

#### Step 2: Research Specific Schools

```bash
# Deep dive into top choices
university-chat --query "Tell me about MIT's computer science program and campus culture"
university-chat --query "What makes Stanford unique for CS students?"
university-chat --query "Compare Carnegie Mellon vs UC Berkeley for computer science"
```

**Example Output**:
```
🤖 MIT is renowned for its cutting-edge CS program with strong emphasis on:
   • Theoretical foundations and research opportunities
   • Entrepreneurship (close to startups in Cambridge/Boston)
   • Interdisciplinary programs (CS + Biology, CS + Economics)
   • Student enrollment: 11,520 | Ranking: #1 World

   Notable programs: Artificial Intelligence Lab, Computer Science and Artificial
   Intelligence Laboratory (CSAIL)
```

#### Step 3: Find Scholarships for Each School

```bash
# National scholarships (applicable to any school)
scholarship-recommend --country "United States" --level Undergraduate \
  --field "Computer Science" --min-amount 5000 --n 20

# High-value full-ride scholarships
scholarship-recommend --min-amount 40000 --renewable --type Merit-based

# Ask about specific opportunities
scholarship-chat --query "What are the best scholarships for computer science undergraduates?"
scholarship-chat --query "Tell me about Gates Millennium Scholars"
```

#### Step 4: Track Applications with Todo App

```bash
# Create application timeline
todo-app add "Stanford REA application - Deadline: Nov 1"
todo-app add "MIT application - Deadline: Nov 1"
todo-app add "Gates Millennium Scholars - Deadline: Sept 15"
todo-app add "Request recommendation letters - By Oct 1"
todo-app add "Write personal statement - By Oct 15"

# Check progress
todo-app list
```

**Result**: Sarah has a balanced list of 15 universities and 10 scholarship applications, all tracked in her todo list.

---

### Example 2: International Student Seeking Graduate Programs

**Background**: Rajesh from India wants to pursue a PhD in Machine Learning in the US or UK.

#### Complete Workflow

```bash
# Step 1: Research top ML programs
university-chat --query "Best universities for PhD in Machine Learning"
university-chat --query "Compare US vs UK for AI research"

# Step 2: Find universities with strong AI research
university-recommend --max-rank 30 --limit 20
universities --search "artificial intelligence" --country "United States"
universities --search "machine learning" --country "United Kingdom"

# Step 3: Find international student scholarships
scholarship-recommend --type "International Students" --level "PhD" --field "Computer Science"
scholarship-chat --query "Best scholarships for international PhD students in AI"
scholarship-chat --query "Tell me about Fulbright program for PhD"

# Step 4: Research funding requirements
scholarship-chat --query "Do most PhD programs provide funding?"
university-chat --query "Which universities offer full funding for PhD students?"

# Step 5: Compare specific programs
university-chat --query "Compare Stanford vs MIT vs CMU for machine learning research"
university-chat --query "What are the advantages of UK PhD programs vs US PhD programs?"
```

**Example Output**:
```
📊 International Student Scholarships Found: 318

Top Recommendations:
1. Fulbright Foreign Student Program
   Amount: $30,000 (renewable)
   Coverage: All international students
   Level: Graduate/PhD

2. AAUW International Fellowships
   Amount: $18,000
   For: Women pursuing graduate degrees

3. Joint Japan/World Bank Graduate Scholarship
   Amount: Full tuition + stipend
   For: Students from developing countries
```

---

### Example 3: Transfer Student Scenario

**Background**: Maria wants to transfer from community college to a 4-year university for Engineering.

```bash
# Step 1: Find transfer-friendly universities
university-recommend --type Public --max-rank 100 --min-students 15000
universities --country "United States" --search "engineering"

# Step 2: Research transfer requirements
university-chat --query "Which universities have the best transfer acceptance rates?"
university-chat --query "What do I need to transfer into engineering programs?"

# Step 3: Find transfer-specific scholarships
scholarship-recommend --type "Transfer Students" --field Engineering
scholarship-chat --query "Scholarships for community college transfer students"
scholarship-chat --query "Show me engineering scholarships for transfer students"

# Step 4: Regional options (California example)
universities --search "California" --limit 30
scholarship-recommend --country "United States" --field Engineering --max-amount 25000
```

---

## Developer Examples

### Example 4: Building a University Comparison Website

**Goal**: Create a web app that helps students compare universities side-by-side.

#### Backend Integration

```python
# app.py - Flask/FastAPI example
from flask import Flask, request, jsonify
from ai_native_playground.universities import UniversityRecommendationModel
from ai_native_playground.universities.llm_chat import UniversityChatbot

app = Flask(__name__)

# Load models
uni_model = UniversityRecommendationModel()
uni_model.load_model("path/to/university_recommendation_model_4k.pkl")

chatbot = UniversityChatbot()

@app.route('/api/universities/similar/<name>')
def find_similar(name):
    """Find universities similar to the given one"""
    results = uni_model.find_similar(name, n_recommendations=10)
    return jsonify(results)

@app.route('/api/universities/recommend', methods=['POST'])
def recommend():
    """Get recommendations based on preferences"""
    preferences = request.json
    results = uni_model.recommend_by_preferences(preferences, n_recommendations=20)
    return jsonify(results)

@app.route('/api/universities/chat', methods=['POST'])
def chat():
    """Chat with AI about universities"""
    query = request.json.get('query')
    response = chatbot.chat(query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

#### Frontend Usage

```javascript
// React/Vue/Angular example
async function findSimilarUniversities(universityName) {
  const response = await fetch(
    `/api/universities/similar/${encodeURIComponent(universityName)}`
  );
  const universities = await response.json();
  return universities;
}

async function getRecommendations(preferences) {
  const response = await fetch('/api/universities/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(preferences)
  });
  return await response.json();
}

async function chatAboutUniversities(question) {
  const response = await fetch('/api/universities/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: question })
  });
  return await response.json();
}

// Usage
const similar = await findSimilarUniversities("Harvard University");
console.log(similar); // [Stanford, Yale, Princeton, ...]

const recommendations = await getRecommendations({
  type: 'Private',
  max_rank: 50,
  min_students: 5000
});
```

---

### Example 5: Scholarship Alert Bot (Discord/Slack)

**Goal**: Create a bot that notifies users about relevant scholarships.

```python
# scholarship_bot.py
import discord
from ai_native_playground.scholarships import ScholarshipRecommendationModel
from ai_native_playground.scholarships.llm_chat import ScholarshipChatbot

client = discord.Client()
scholarship_model = ScholarshipRecommendationModel()
scholarship_model.load_model("path/to/scholarship_recommendation_model.pkl")
chatbot = ScholarshipChatbot()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command: !scholarships <field> <country>
    if message.content.startswith('!scholarships'):
        parts = message.content.split()
        field = parts[1] if len(parts) > 1 else None
        country = parts[2] if len(parts) > 2 else None

        preferences = {}
        if field:
            preferences['field'] = field
        if country:
            preferences['country'] = country

        scholarships = scholarship_model.recommend_by_preferences(
            preferences,
            n_recommendations=5
        )

        response = "📚 **Scholarship Recommendations**\n\n"
        for i, s in enumerate(scholarships, 1):
            response += f"{i}. **{s['name']}**\n"
            response += f"   💰 ${s['amount']:,}\n"
            response += f"   🌍 {s['country']} | 📚 {s['field']}\n\n"

        await message.channel.send(response)

    # Command: !ask <question>
    elif message.content.startswith('!ask'):
        query = message.content[5:]  # Remove "!ask "
        result = chatbot.chat(query)
        await message.channel.send(result['response'])

client.run('YOUR_BOT_TOKEN')
```

**Usage in Discord**:
```
User: !scholarships Engineering USA
Bot:  📚 Scholarship Recommendations

      1. MIT Merit Scholarship
         💰 $59,349
         🌍 United States | 📚 Engineering

      2. Stanford Excellence Award
         💰 $45,000
         🌍 United States | 📚 Engineering

User: !ask Tell me about Fulbright
Bot:  The Fulbright Program is a prestigious international educational
      exchange scholarship...
```

---

### Example 6: Automated Weather + News Dashboard

**Goal**: Daily digest combining weather, news, and tasks.

```bash
#!/bin/bash
# daily_digest.sh

echo "================================"
echo "📅 DAILY DIGEST - $(date '+%B %d, %Y')"
echo "================================"
echo ""

# Weather
echo "🌤️  WEATHER FORECAST"
echo "-------------------"
curl -s "http://localhost:8000/current?city=Boston" | jq '.temperature, .weather_main'
echo ""

# News
echo "📰 TOP TECH NEWS"
echo "----------------"
news-analyzer --quick --max-headlines 5
echo ""

# Tasks
echo "✅ TODAY'S TASKS"
echo "---------------"
todo-app list
echo ""

# University deadlines (custom)
echo "🎓 UPCOMING DEADLINES"
echo "--------------------"
echo "• Stanford REA - November 1"
echo "• MIT Application - November 1"
echo ""

# Scholarship opportunities
echo "💰 NEW SCHOLARSHIPS"
echo "------------------"
scholarship-recommend --min-amount 30000 --n 3 | grep "name\|Amount"
echo ""

echo "================================"
echo "Have a productive day! 🚀"
```

Run daily:
```bash
chmod +x daily_digest.sh
./daily_digest.sh

# Or automate with cron
crontab -e
# Add: 0 8 * * * /path/to/daily_digest.sh
```

---

## Researcher Examples

### Example 7: Comparative Education Research

**Goal**: Compare higher education systems across countries.

```bash
# Step 1: Export data for each country
universities --country "United States" --export data/us_universities.json
universities --country "United Kingdom" --export data/uk_universities.json
universities --country "Germany" --export data/de_universities.json
universities --country "China" --export data/cn_universities.json
universities --country "India" --export data/in_universities.json

# Step 2: Get statistics for each
university-chat --stats > data/university_statistics.txt
scholarship-chat --stats > data/scholarship_statistics.txt

# Step 3: Analyze with Python
```

```python
# analysis.py
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
countries = ['us', 'uk', 'de', 'cn', 'in']
dataframes = {}

for country in countries:
    with open(f'data/{country}_universities.json') as f:
        data = json.load(f)
        dataframes[country] = pd.DataFrame(data)

# Comparative analysis
print("=== UNIVERSITY COMPARISON BY COUNTRY ===\n")

for country, df in dataframes.items():
    print(f"\n{country.upper()}:")
    print(f"  Total Universities: {len(df)}")
    print(f"  Avg Students: {df['students'].mean():.0f}")
    print(f"  Avg Ranking: {df['ranking'].mean():.1f}")
    print(f"  Public vs Private: {df['type'].value_counts().to_dict()}")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: University count by country
counts = {c: len(df) for c, df in dataframes.items()}
axes[0, 0].bar(counts.keys(), counts.values())
axes[0, 0].set_title('Number of Universities by Country')

# Plot 2: Average ranking
avg_rankings = {c: df['ranking'].mean() for c, df in dataframes.items()}
axes[0, 1].bar(avg_rankings.keys(), avg_rankings.values())
axes[0, 1].set_title('Average University Ranking')

# Plot 3: Student population distribution
for country, df in dataframes.items():
    axes[1, 0].hist(df['students'], alpha=0.5, label=country)
axes[1, 0].set_title('Student Population Distribution')
axes[1, 0].legend()

# Plot 4: Type distribution
type_data = {}
for country, df in dataframes.items():
    type_data[country] = df['type'].value_counts()
pd.DataFrame(type_data).plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('University Types by Country')

plt.tight_layout()
plt.savefig('university_comparison.png')
print("\n✅ Visualization saved as 'university_comparison.png'")
```

**Expected Output**:
```
=== UNIVERSITY COMPARISON BY COUNTRY ===

US:
  Total Universities: 700
  Avg Students: 28,543
  Avg Ranking: 245.2
  Public vs Private: {'Public': 420, 'Private': 280}

UK:
  Total Universities: 300
  Avg Students: 18,765
  Avg Ranking: 189.3
  Public vs Private: {'Public': 245, 'Private': 55}

...
```

---

### Example 8: Scholarship Funding Analysis

**Goal**: Analyze scholarship availability and funding trends.

```python
# scholarship_analysis.py
from ai_native_playground.scholarships.ml_model import ScholarshipRecommendationModel
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load scholarship data
model = ScholarshipRecommendationModel()
model.load_model("path/to/scholarship_recommendation_model.pkl")

scholarships = model.scholarships
df = pd.DataFrame(scholarships)

print("=== SCHOLARSHIP FUNDING ANALYSIS ===\n")

# Basic statistics
print(f"Total Scholarships: {len(df)}")
print(f"Total Funding Available: ${df['amount'].sum():,.0f}")
print(f"Average Award: ${df['amount'].mean():,.0f}")
print(f"Median Award: ${df['amount'].median():,.0f}")
print(f"Max Award: ${df['amount'].max():,.0f}")
print(f"\nRenewable Scholarships: {df['renewable'].sum()} ({df['renewable'].sum()/len(df)*100:.1f}%)")

# Analysis by field
print("\n=== FUNDING BY FIELD ===")
field_analysis = df.groupby('field').agg({
    'amount': ['count', 'mean', 'sum']
}).round(0)
print(field_analysis.sort_values(('amount', 'sum'), ascending=False).head(10))

# Analysis by country
print("\n=== FUNDING BY COUNTRY ===")
country_analysis = df.groupby('country').agg({
    'amount': ['count', 'mean', 'sum']
}).round(0)
print(country_analysis.sort_values(('amount', 'sum'), ascending=False).head(10))

# Renewable vs Non-renewable
print("\n=== RENEWABLE vs NON-RENEWABLE ===")
renewable_stats = df.groupby('renewable')['amount'].agg(['count', 'mean', 'sum'])
print(renewable_stats)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Distribution of scholarship amounts
axes[0, 0].hist(df['amount'], bins=50, edgecolor='black')
axes[0, 0].set_title('Distribution of Scholarship Amounts')
axes[0, 0].set_xlabel('Amount ($)')
axes[0, 0].set_ylabel('Frequency')

# Plot 2: Top 10 fields by total funding
top_fields = df.groupby('field')['amount'].sum().sort_values(ascending=False).head(10)
axes[0, 1].barh(top_fields.index, top_fields.values)
axes[0, 1].set_title('Top 10 Fields by Total Funding')
axes[0, 1].set_xlabel('Total Funding ($)')

# Plot 3: Scholarship count by country
country_counts = df['country'].value_counts().head(15)
axes[1, 0].bar(range(len(country_counts)), country_counts.values)
axes[1, 0].set_xticks(range(len(country_counts)))
axes[1, 0].set_xticklabels(country_counts.index, rotation=45, ha='right')
axes[1, 0].set_title('Scholarship Count by Country (Top 15)')
axes[1, 0].set_ylabel('Count')

# Plot 4: Average amount by level
level_avg = df.groupby('level')['amount'].mean().sort_values(ascending=False)
axes[1, 1].bar(level_avg.index, level_avg.values)
axes[1, 1].set_title('Average Scholarship Amount by Education Level')
axes[1, 1].set_ylabel('Average Amount ($)')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('scholarship_analysis.png', dpi=300)
print("\n✅ Visualization saved as 'scholarship_analysis.png'")

# Generate report
with open('scholarship_report.txt', 'w') as f:
    f.write("SCHOLARSHIP FUNDING ANALYSIS REPORT\n")
    f.write("="*60 + "\n\n")
    f.write(f"Total Scholarships Analyzed: {len(df)}\n")
    f.write(f"Total Funding Available: ${df['amount'].sum():,.0f}\n")
    f.write(f"Average Award: ${df['amount'].mean():,.0f}\n\n")
    f.write("Top 10 Fields by Funding:\n")
    f.write(str(top_fields))

print("✅ Report saved as 'scholarship_report.txt'")
```

---

## Professional Examples

### Example 9: Education Consultant Tool

**Background**: You're an education consultant helping 20 students simultaneously.

```bash
# Create a client management system
mkdir clients

# For each client, create a profile
cat > clients/client_001.sh << 'EOF'
#!/bin/bash
# Client: Sarah Johnson
# Profile: CS major, needs scholarships, GPA: 3.8

CLIENT="Sarah Johnson"
FIELD="Computer Science"
COUNTRY="United States"
LEVEL="Undergraduate"
MIN_SCHOLARSHIP=15000

echo "=== Client Profile: $CLIENT ==="
echo ""

echo "📚 University Recommendations:"
university-recommend --max-rank 50 --limit 10

echo ""
echo "💰 Scholarship Recommendations:"
scholarship-recommend --country "$COUNTRY" \
  --field "$FIELD" \
  --level "$LEVEL" \
  --min-amount $MIN_SCHOLARSHIP \
  --n 15

echo ""
echo "🎯 Personalized Insights:"
university-chat --query "Best universities for $FIELD major with strong internship programs"
scholarship-chat --query "Merit scholarships for $FIELD students with GPA above 3.5"
EOF

chmod +x clients/client_001.sh
./clients/client_001.sh > reports/client_001_report.txt
```

---

### Example 10: University Admissions Office Analytics

**Goal**: Understand competitor universities for recruitment strategies.

```bash
# Identify peer institutions
university-recommend --similar "Boston University" --limit 20

# Analyze scholarship competitiveness
scholarship-chat --query "What scholarships are offered by top 50 universities?"

# Compare with similar institutions
university-chat --query "Compare Boston University with Northeastern, NYU, and GWU"

# Export for detailed analysis
universities --search "Boston" --export peer_institutions.json
```

```python
# competitive_analysis.py
import json
import pandas as pd

# Load your university and competitors
with open('peer_institutions.json') as f:
    peers = json.load(f)

df = pd.DataFrame(peers)

print("=== COMPETITIVE ANALYSIS ===\n")
print("Peer Institutions:")
for _, row in df.iterrows():
    print(f"\n{row['name']}:")
    print(f"  Ranking: {row['ranking']}")
    print(f"  Students: {row['students']:,}")
    print(f"  Type: {row['type']}")
    print(f"  Founded: {row['founded']}")

# Identify strengths and weaknesses
print("\n=== COMPETITIVE POSITIONING ===")
print(f"Your Avg Ranking: {df[df['name'].str.contains('Boston U')]['ranking'].values[0]}")
print(f"Peer Avg Ranking: {df[~df['name'].str.contains('Boston U')]['ranking'].mean():.1f}")
print(f"Your Enrollment: {df[df['name'].str.contains('Boston U')]['students'].values[0]:,}")
print(f"Peer Avg Enrollment: {df[~df['name'].str.contains('Boston U')]['students'].mean():.0f}")
```

---

## Advanced Workflows

### Example 11: Complete Student Journey Automation

**Goal**: Automate the entire university search → application → scholarship hunt process.

```bash
#!/bin/bash
# student_journey.sh

STUDENT_NAME="Alex Chen"
FIELD="Engineering"
COUNTRY="United States"
GPA=3.9
MIN_SCHOLARSHIP=20000

echo "========================================="
echo "🎓 COMPLETE UNIVERSITY APPLICATION PLAN"
echo "   Student: $STUDENT_NAME"
echo "   Field: $FIELD | GPA: $GPA"
echo "========================================="

# Phase 1: University Research
echo -e "\n📚 PHASE 1: UNIVERSITY RESEARCH\n"

echo "Finding reach schools (top 30)..."
university-recommend --max-rank 30 --limit 10 > phase1_reach.txt

echo "Finding match schools (rank 30-70)..."
university-recommend --min-rank 30 --max-rank 70 --limit 10 > phase1_match.txt

echo "Finding safety schools (rank 70-150)..."
university-recommend --min-rank 70 --max-rank 150 --limit 10 > phase1_safety.txt

# Phase 2: Detailed Research
echo -e "\n🔍 PHASE 2: DETAILED ANALYSIS\n"

university-chat --query "What are the best $FIELD programs in the US?" > phase2_programs.txt
university-chat --query "Which universities have the highest job placement for $FIELD?" >> phase2_programs.txt

# Phase 3: Scholarship Search
echo -e "\n💰 PHASE 3: SCHOLARSHIP HUNTING\n"

echo "Finding high-value scholarships..."
scholarship-recommend --country "$COUNTRY" --field "$FIELD" \
  --level Undergraduate --min-amount $MIN_SCHOLARSHIP \
  --renewable --n 30 > phase3_scholarships.txt

echo "Finding university-specific scholarships..."
scholarship-chat --query "Show me scholarships offered by top engineering schools" >> phase3_scholarships.txt

echo "Finding merit scholarships for high GPA students..."
scholarship-chat --query "Merit scholarships for $FIELD students with GPA above 3.8" >> phase3_scholarships.txt

# Phase 4: Application Timeline
echo -e "\n📅 PHASE 4: APPLICATION TIMELINE\n"

# Create todos for each deadline
todo-app add "Research universities - Complete by August 1"
todo-app add "Draft personal statement - Complete by September 1"
todo-app add "Request recommendation letters - By September 15"
todo-app add "Complete Common App - By October 1"
todo-app add "Submit early action applications - By November 1"
todo-app add "Submit scholarship applications - By November 15"
todo-app add "Submit regular decision applications - By January 1"

todo-app list > phase4_timeline.txt

# Phase 5: Generate Report
echo -e "\n📋 PHASE 5: GENERATING COMPREHENSIVE REPORT\n"

cat > final_report.md << EOF
# University Application Plan for $STUDENT_NAME

## Profile
- **Field**: $FIELD
- **GPA**: $GPA
- **Target Country**: $COUNTRY
- **Scholarship Need**: Minimum \$$MIN_SCHOLARSHIP

## University List

### Reach Schools (Top 30)
$(cat phase1_reach.txt | head -30)

### Match Schools (Rank 30-70)
$(cat phase1_match.txt | head -30)

### Safety Schools (Rank 70-150)
$(cat phase1_safety.txt | head -30)

## Program Insights
$(cat phase2_programs.txt)

## Scholarship Opportunities
$(cat phase3_scholarships.txt | head -50)

## Application Timeline
$(cat phase4_timeline.txt)

## Next Steps
1. Visit university websites for specific requirements
2. Prepare application materials
3. Apply for scholarships with earliest deadlines first
4. Track all deadlines using todo-app

---
Generated on: $(date)
EOF

echo "✅ COMPLETE! Check final_report.md for your personalized plan."
echo ""
echo "Summary:"
echo "  - Universities researched: 30"
echo "  - Scholarships found: 30+"
echo "  - Application tasks created: 7"
echo "  - Comprehensive report: final_report.md"
```

Run it:
```bash
chmod +x student_journey.sh
./student_journey.sh
```

---

### Example 12: Multi-Student Batch Processing

**Goal**: Process scholarship recommendations for 100 students efficiently.

```python
# batch_recommendations.py
import csv
import json
from ai_native_playground.scholarships import ScholarshipRecommendationModel

# Load model
model = ScholarshipRecommendationModel()
model.load_model("path/to/scholarship_recommendation_model.pkl")

# Load student profiles from CSV
students = []
with open('students.csv', 'r') as f:
    reader = csv.DictReader(f)
    students = list(reader)

# Process each student
results = {}

for student in students:
    student_id = student['id']
    preferences = {
        'country': student['country'],
        'field': student['field'],
        'level': student['level'],
        'min_amount': int(student['min_amount'])
    }

    # Get recommendations
    recommendations = model.recommend_by_preferences(preferences, n_recommendations=10)
    results[student_id] = recommendations

    print(f"✅ Processed student {student_id}: Found {len(recommendations)} scholarships")

# Save results
with open('batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Generate individual reports
for student_id, scholarships in results.items():
    with open(f'reports/student_{student_id}_scholarships.txt', 'w') as f:
        f.write(f"SCHOLARSHIP RECOMMENDATIONS - Student {student_id}\n")
        f.write("="*60 + "\n\n")

        for i, s in enumerate(scholarships, 1):
            f.write(f"{i}. {s['name']}\n")
            f.write(f"   Amount: ${s['amount']:,}\n")
            f.write(f"   Provider: {s['provider']}\n")
            f.write(f"   Country: {s['country']}\n")
            f.write(f"   Field: {s['field']} | Level: {s['level']}\n\n")

print(f"\n✅ Batch processing complete! Processed {len(students)} students.")
print(f"✅ Results saved to batch_results.json")
print(f"✅ Individual reports in reports/ directory")
```

**students.csv format**:
```csv
id,name,country,field,level,min_amount
001,John Doe,United States,Engineering,Undergraduate,15000
002,Jane Smith,Canada,Medicine,Graduate,25000
003,Alex Lee,United Kingdom,Computer Science,PhD,30000
...
```

---

## Tips for Maximum Efficiency

### 1. **Create Aliases for Frequent Commands**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias uni-search='university-recommend'
alias uni-chat='university-chat --query'
alias scholar-search='scholarship-recommend'
alias scholar-chat='scholarship-chat --query'
alias my-tasks='todo-app list'
alias add-task='todo-app add'

# Usage
uni-search --similar "MIT" --limit 10
scholar-search --field Engineering --min-amount 30000
```

### 2. **Combine Tools with Shell Pipes**

```bash
# Find universities, extract names, search scholarships
universities --country "United States" --limit 50 | \
  grep "name:" | \
  head -10

# Export and count
universities --export all.json && \
  echo "Total universities: $(jq '. | length' all.json)"
```

### 3. **Schedule Regular Updates**

```bash
# Add to crontab for weekly scholarship alerts
0 9 * * 1 scholarship-recommend --renewable --min-amount 25000 | mail -s "Weekly Scholarship Digest" your@email.com
```

---

**More Examples Coming Soon!**

Have a specific use case? Open an issue or PR with your example!

---

[Back to README](README.md) | [Quick Start Guide](QUICKSTART.md)
