# 🚀 Quick Start Guide - AI Native Playground

Get up and running with the most powerful features in under 5 minutes!

## Table of Contents
- [Installation](#installation)
- [Common Workflows](#common-workflows)
- [For Students](#for-students)
- [For Developers](#for-developers)
- [For Researchers](#for-researchers)
- [Tips & Tricks](#tips--tricks)

---

## Installation

### Quick Setup (3 steps)
```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd ai-native-playground

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install
pip install -e .
```

### Optional: Configure OpenAI (for LLM features)
```bash
# Copy environment template
cp .env.example .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your-key-here" >> .env

# Or export directly
export OPENAI_API_KEY='your-key-here'
```

---

## Common Workflows

### 🎓 Workflow 1: Find Your Dream University (3 minutes)

**Goal**: Discover universities that match your profile and interests.

```bash
# Step 1: Search for top universities in your field
university-chat --query "What are the best computer science universities in the US?"

# Step 2: Find similar universities to your favorite
university-recommend --similar "MIT" --limit 10

# Step 3: Get recommendations based on your preferences
university-recommend --type Private --max-rank 50 --min-students 5000

# Step 4: Explore specific countries
universities --country "United States" --search "engineering" --limit 20
```

**Example Output**:
```
1. Massachusetts Institute of Technology (MIT)
   Ranking: 1 | Students: 11,520 | Type: Private
   Location: Cambridge, MA

2. Stanford University
   Ranking: 3 | Students: 17,000 | Type: Private
   Location: Stanford, CA
```

---

### 💰 Workflow 2: Find Scholarships You Qualify For (5 minutes)

**Goal**: Discover scholarships matching your profile and maximize financial aid.

```bash
# Step 1: Start with interactive recommendations
scholarship-recommend
# Answer: Country: United States
# Answer: Field: Computer Science
# Answer: Level: Graduate
# Answer: Min Amount: 25000

# Step 2: Refine with specific filters
scholarship-recommend --country "United States" \
  --field "Computer Science" \
  --level Graduate \
  --min-amount 25000 \
  --renewable

# Step 3: Ask the chatbot for specific advice
scholarship-chat --query "Show me renewable scholarships for CS graduate students"

# Step 4: Research major scholarships
scholarship-chat --query "Tell me about NSF Graduate Research Fellowship"
```

**Pro Tips**:
- Use `--renewable` flag for multi-year support
- Set realistic `--min-amount` to avoid wasting time
- Check `--stats` to see what's available in your field

---

### 🎯 Workflow 3: Complete University + Scholarship Search (10 minutes)

**Goal**: Find both universities AND scholarships in one workflow.

```bash
# Step 1: Find target universities
university-recommend --type Private --max-rank 100 --limit 20 > my_universities.txt

# Step 2: Search for universities in specific country
universities --country "United Kingdom" --limit 30

# Step 3: Find scholarships for that country
scholarship-recommend --country "United Kingdom" --level Graduate --n 20

# Step 4: Ask specific questions
university-chat --query "Compare Oxford and Cambridge for engineering"
scholarship-chat --query "What scholarships are available for UK universities?"

# Step 5: Check scholarship deadlines and amounts
scholarship-recommend --country "United Kingdom" --min-amount 20000 --renewable
```

---

### 📊 Workflow 4: Data Export & Analysis (For Research)

**Goal**: Export datasets for your own analysis.

```bash
# Export all universities
universities --export all_universities.json

# Export specific country
universities --country "Germany" --export german_universities.json

# View statistics
universities --stats
scholarship-chat --stats

# Generate custom datasets
python -m ai_native_playground.universities.generate_4000_data
python -m ai_native_playground.scholarships.generate_scholarships
```

**Use Cases**:
- Machine learning research
- Educational data analysis
- Comparative studies
- Custom visualizations

---

### 🌤️ Workflow 5: Daily Productivity Tools

**Goal**: Quick access to weather, news, and tasks.

```bash
# Morning routine:
# 1. Check weather
weather-api &  # Runs in background
# Access at http://localhost:8000

# 2. Get news digest
news-analyzer --quick

# 3. Check your todos
todo-app list

# 4. Add new tasks
todo-app add "Apply to Stanford scholarship"
todo-app add "Email professor about recommendation letter"
```

---

## For Students

### 🎓 College Application Season

**Timeline**: Start 12-18 months before enrollment

```bash
# Month 1-3: Research Phase
# -------------------------
# Build your university list
university-recommend --type Private --max-rank 100 --limit 30
university-recommend --type Public --max-rank 50 --limit 20

# Research each university
university-chat --query "Tell me about Stanford's computer science program"
university-chat --query "What makes MIT unique for engineering students?"

# Month 4-6: Scholarship Search
# -----------------------------
# Find scholarships by deadline
scholarship-recommend --country "United States" --level Undergraduate
scholarship-chat --query "Show me scholarships with fall deadlines"

# Research major scholarships
scholarship-chat --query "Tell me about Gates Millennium Scholars program"
scholarship-recommend --similar "Gates Millennium Scholars"

# Month 7-12: Applications
# ------------------------
# Track applications
todo-app add "Submit MIT application - Deadline: Nov 1"
todo-app add "Apply for Fulbright scholarship - Deadline: Oct 15"
todo-app list

# Get inspiration
university-chat --query "What do admissions officers look for at top universities?"
```

---

### 📚 Graduate School Planning

```bash
# Research graduate programs
university-chat --query "Best universities for PhD in Machine Learning"
university-recommend --max-rank 50 --min-students 10000

# Find graduate scholarships
scholarship-recommend --level Graduate --field "Computer Science" --min-amount 30000
scholarship-recommend --level "PhD" --type Research --renewable

# Compare programs
university-chat --query "Compare Stanford vs MIT for AI research"
scholarship-chat --query "Best fellowships for STEM PhD students"
```

---

### 🌍 International Student Guide

```bash
# Research universities in different countries
universities --country "United States" --limit 50
universities --country "United Kingdom" --limit 50
universities --country "Canada" --limit 50

# Find international student scholarships
scholarship-recommend --type "International Students" --min-amount 20000
scholarship-chat --query "Scholarships for international students in the US"

# Compare countries
university-chat --query "Compare studying in US vs UK for engineering"
scholarship-chat --query "Which countries offer the most scholarships for international students?"
```

---

## For Developers

### 🔌 API Integration Examples

#### Weather API
```bash
# Start the server
weather-api &

# Test endpoints
curl "http://localhost:8000/current?city=London"
curl "http://localhost:8000/forecast?city=Tokyo"

# Integration example
curl -s "http://localhost:8000/current?city=Berlin" | jq '.temperature'
```

#### Reddit Sentiment API
```bash
# Start the service
reddit-sentiment &

# Analyze sentiment
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/technology/comments/xyz/", "max_comments": 100}'
```

---

### 🤖 ML Model Integration

```python
# Example: Use university recommendation model in your code
from ai_native_playground.universities import UniversityRecommendationModel

model = UniversityRecommendationModel()
model.load_model("path/to/model.pkl")

# Get recommendations
similar = model.find_similar("Harvard University", n_recommendations=10)
print(similar)
```

```python
# Example: Use scholarship recommendation model
from ai_native_playground.scholarships import ScholarshipRecommendationModel

model = ScholarshipRecommendationModel()
model.load_model("path/to/scholarship_model.pkl")

# Filter by preferences
preferences = {
    'country': 'United States',
    'field': 'Engineering',
    'min_amount': 25000
}
recommendations = model.recommend_by_preferences(preferences, n_recommendations=10)
```

---

### 📊 Data Science Projects

```bash
# Export datasets for analysis
universities --export data/universities.json
scholarship-chat --stats > data/scholarship_stats.txt

# Load in Python
import json
with open('data/universities.json') as f:
    universities = json.load(f)

# Analyze with pandas
import pandas as pd
df = pd.DataFrame(universities)
print(df.describe())
print(df.groupby('country')['ranking'].mean())
```

---

## For Researchers

### 📈 Dataset Collection

```bash
# Collect comprehensive datasets
universities --export research/universities_full.json
python -m ai_native_playground.universities.generate_4000_data
python -m ai_native_playground.scholarships.generate_scholarships

# View dataset statistics
echo "=== University Statistics ===" > research/stats.txt
university-chat --stats >> research/stats.txt

echo "\n=== Scholarship Statistics ===" >> research/stats.txt
scholarship-chat --stats >> research/stats.txt
```

---

### 🔬 Comparative Analysis

```bash
# Compare education systems
university-chat --query "Compare higher education systems in US vs Europe"
university-chat --query "What are the differences between Asian and Western universities?"

# Scholarship availability by region
scholarship-chat --query "Which countries offer the most scholarships?"
scholarship-chat --query "Compare merit-based vs need-based scholarships globally"

# Export for statistical analysis
universities --country "United States" --export us_universities.json
universities --country "United Kingdom" --export uk_universities.json
universities --country "Germany" --export de_universities.json
```

---

## Tips & Tricks

### 💡 Power User Tips

#### 1. **Combine Multiple Filters for Precision**
```bash
# Find your exact match
scholarship-recommend \
  --country "Canada" \
  --field "Computer Science" \
  --level Graduate \
  --min-amount 25000 \
  --max-amount 50000 \
  --renewable \
  --n 20
```

#### 2. **Use Similarity Search for Alternatives**
```bash
# Found your dream school but need backups?
university-recommend --similar "MIT" --limit 20

# Like one scholarship? Find similar ones
scholarship-recommend --similar "Fulbright Program"
```

#### 3. **Export and Process with Shell Tools**
```bash
# Find all top CS schools and their scholarships
universities --search "computer" --country "United States" > cs_schools.txt
scholarship-recommend --field "Computer Science" --min-amount 20000 > cs_scholarships.txt

# Count results
wc -l cs_schools.txt cs_scholarships.txt
```

#### 4. **Interactive Mode for Exploration**
```bash
# When unsure, use interactive mode
scholarship-recommend
# Answer questions step by step

university-chat
# Type: help
# Type: What are the best engineering schools?
```

#### 5. **Use Stats to Understand Availability**
```bash
# Before searching, understand what's available
scholarship-chat --stats
# Look at distribution by country, field, level

university-chat --stats
# See coverage by country and type
```

---

### ⚡ Quick Commands Cheat Sheet

| Task | Command |
|------|---------|
| **Find scholarships** | `scholarship-recommend --country US --field Engineering` |
| **Chat about universities** | `university-chat --query "Tell me about MIT"` |
| **Similar universities** | `university-recommend --similar "Stanford"` |
| **High-value scholarships** | `scholarship-recommend --min-amount 40000 --renewable` |
| **Export data** | `universities --export mydata.json` |
| **View statistics** | `scholarship-chat --stats` |
| **Add task** | `todo-app add "Apply to scholarships"` |
| **Get news** | `news-analyzer --quick` |
| **Check weather** | `weather-api` (then visit localhost:8000) |
| **Analyze Reddit** | `reddit-sentiment` (then visit localhost:8001) |

---

### 🔧 Troubleshooting

**Problem**: "Model not found" error
```bash
# Solution: Generate the datasets first
python -m ai_native_playground.universities.generate_4000_data
python -m ai_native_playground.scholarships.generate_scholarships
```

**Problem**: LLM responses are basic/generic
```bash
# Solution: Set your OpenAI API key
export OPENAI_API_KEY='your-actual-key-here'
```

**Problem**: "Command not found"
```bash
# Solution: Install in development mode
pip install -e .

# Or use module syntax
python -m ai_native_playground.scholarships.chat_cli --query "help"
```

---

### 🎯 Next Steps

1. **Explore More**: Try all the commands in this guide
2. **Customize**: Modify the filters to match your needs
3. **Export Data**: Use the data in your own projects
4. **Integrate**: Build apps using the ML models and APIs
5. **Contribute**: Add more features or data sources

---

## Quick Reference Card

```
🎓 UNIVERSITIES                    💰 SCHOLARSHIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
universities --search MIT          scholarship-recommend --field CS
university-recommend --similar MIT scholarship-chat --query "show STEM"
university-chat --query "tell MIT" scholarship-recommend --renewable

🌤️  WEATHER                        📰 NEWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
weather-api                        news-analyzer
curl localhost:8000/current?city=LA news-analyzer --quick

😊 REDDIT SENTIMENT                ✅ TODO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
reddit-sentiment                   todo-app add "task"
visit localhost:8001               todo-app list
```

---

**Need Help?**
- Run any command with `--help` flag
- Check [EXAMPLES.md](EXAMPLES.md) for specific use cases
- See [README.md](README.md) for complete documentation

**Happy exploring! 🚀**
