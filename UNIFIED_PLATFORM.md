# 🎓 AI Education Platform - Unified App

**One powerful API combining 4,550 universities and 4,011 scholarships!**

## Overview

The AI Education Platform is a unified service that combines university recommendations and scholarship search into a single, powerful API. Instead of running separate services, you get everything in one place.

### What's Included

- 🎓 **4,550 Universities** across 20 countries
- 💰 **4,011 Scholarships** across 18 countries
- 🤖 **ML Recommendations** using content-based filtering
- 💬 **AI Chatbot** with Retrieval Augmented Generation (RAG)
- 🔍 **Combined Search** - Find universities and scholarships together!
- ⚡ **Fast API** with sub-second response times
- 🌐 **Web Interface** with beautiful UI

---

## 🚀 Quick Start

### Deploy to Render (Production)

The easiest way to get started - deploy in one click!

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

After deployment, your unified platform will be available at:
```
https://ai-education-platform.onrender.com
```

---

### Run Locally (Development)

```bash
# 1. Install dependencies
pip install -e .

# 2. Generate data (first time only - takes 2-3 minutes)
python -m ai_native_playground.universities.generate_4000_data
python -m ai_native_playground.scholarships.generate_scholarships

# 3. Start the server
uvicorn ai_native_playground.education_platform.app:app --reload

# 4. Open your browser
open http://localhost:8000
```

**That's it!** You now have a complete education platform running locally.

---

## 🎯 Key Features

### 1. **Combined Search** (🔥 Power Feature!)

Search for universities AND scholarships in a single API call. Perfect for students planning their education.

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/search/combined" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "field": "Computer Science",
    "level": "Undergraduate",
    "max_university_rank": 50,
    "min_scholarship_amount": 20000,
    "scholarship_renewable": true,
    "n_universities": 10,
    "n_scholarships": 10
  }'
```

**Response**:
```json
{
  "success": true,
  "universities": {
    "count": 10,
    "results": [
      {
        "name": "Massachusetts Institute of Technology",
        "ranking": 1,
        "students": 11500,
        "type": "Private",
        "founded": 1861
      },
      ...
    ],
    "avg_ranking": 25.4
  },
  "scholarships": {
    "count": 10,
    "results": [
      {
        "name": "NSF Graduate Research Fellowship",
        "amount": 37000,
        "renewable": true,
        "provider": "National Science Foundation",
        "country": "United States"
      },
      ...
    ],
    "total_value": 425000,
    "avg_amount": 42500
  },
  "summary": {
    "total_results": 20,
    "potential_funding": "$425,000",
    "recommendation": "Apply to 10 universities with $425,000 in potential scholarships"
  }
}
```

---

### 2. **AI Chatbot**

Chat naturally with AI about universities, scholarships, or both!

**Example**:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are good engineering schools with renewable scholarships over $30,000?"}'
```

**Response**:
```json
{
  "success": true,
  "query": "What are good engineering schools with renewable scholarships over $30,000?",
  "context": "combined",
  "response": "🎓 UNIVERSITIES:\nTop engineering schools include MIT (ranked #1), Stanford University (#5), and UC Berkeley (#10)...\n\n💰 SCHOLARSHIPS:\nRenewable scholarships over $30,000 include NSF Graduate Research Fellowship ($37,000 annually), Gates Millennium Scholars ($50,000)...",
  "universities_found": 5,
  "scholarships_found": 8,
  "using_llm": true
}
```

The AI automatically determines whether you're asking about universities, scholarships, or both!

---

### 3. **ML-Powered Recommendations**

Get personalized university and scholarship recommendations based on your preferences.

**University Recommendations**:
```bash
curl -X POST "http://localhost:8000/api/universities/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "type": "Private",
    "max_rank": 50,
    "n_recommendations": 10
  }'
```

**Scholarship Recommendations**:
```bash
curl -X POST "http://localhost:8000/api/scholarships/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "field": "Engineering",
    "level": "Graduate",
    "min_amount": 25000,
    "renewable": true,
    "n_recommendations": 15
  }'
```

---

### 4. **Find Similar**

Found a university or scholarship you like? Find similar ones!

```bash
# Find universities similar to MIT
curl -X POST "http://localhost:8000/api/universities/similar" \
  -H "Content-Type: application/json" \
  -d '{"name": "Massachusetts Institute of Technology", "n_recommendations": 10}'

# Find scholarships similar to Fulbright
curl -X POST "http://localhost:8000/api/scholarships/similar" \
  -H "Content-Type: application/json" \
  -d '{"name": "Fulbright Program", "n_recommendations": 10}'
```

---

### 5. **Platform Statistics**

Get comprehensive statistics about the entire platform.

```bash
curl http://localhost:8000/api/stats
```

**Response includes**:
- Total universities and scholarships
- Breakdown by country
- Average rankings and amounts
- Renewable scholarship percentages
- Top fields of study
- And much more!

---

## 📖 Complete API Reference

### Base URL
- **Production**: `https://ai-education-platform.onrender.com`
- **Local**: `http://localhost:8000`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface (beautiful UI) |
| GET | `/health` | Health check |
| GET | `/api/stats` | Platform statistics |
| GET | `/api/docs` | Interactive API documentation |
| POST | `/api/search/combined` | **🔥 Search universities + scholarships** |
| POST | `/api/universities/recommend` | Get university recommendations |
| POST | `/api/universities/similar` | Find similar universities |
| POST | `/api/scholarships/recommend` | Get scholarship recommendations |
| POST | `/api/scholarships/similar` | Find similar scholarships |
| POST | `/api/chat` | Chat with AI about education |

---

## 🌐 Web Interface

The platform includes a beautiful web interface accessible at the root URL.

**Features**:
- 📊 Platform statistics at a glance
- 🔗 Quick links to API documentation
- 📚 Example API usage
- 🎨 Modern, responsive design

Simply visit `http://localhost:8000` (or your deployed URL) in your browser!

---

## 💻 Frontend Integration

### JavaScript/React Example

```javascript
const API_BASE = 'https://ai-education-platform.onrender.com';

// Combined search
async function searchEducation(criteria) {
  const response = await fetch(`${API_BASE}/api/search/combined`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(criteria)
  });
  return await response.json();
}

// Example usage
const results = await searchEducation({
  country: "United States",
  field: "Computer Science",
  max_university_rank: 50,
  min_scholarship_amount: 20000,
  scholarship_renewable: true,
  n_universities: 10,
  n_scholarships: 10
});

console.log(`Found ${results.universities.count} universities`);
console.log(`Found ${results.scholarships.count} scholarships`);
console.log(`Total funding: ${results.summary.potential_funding}`);
```

### Chat Integration

```javascript
async function chatWithAI(question) {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: question })
  });

  const data = await response.json();
  return data.response;
}

// Example
const answer = await chatWithAI("What are the best CS programs in California?");
console.log(answer);
```

---

## 🔧 Configuration

### Environment Variables

```env
# Optional: For enhanced LLM chatbot features
OPENAI_API_KEY=your_openai_api_key_here

# Python version (for Render)
PYTHON_VERSION=3.11.0
```

**Note**: The platform works without OpenAI API key - chatbot uses fallback mode.

---

## 📊 Data Coverage

### Universities (4,550 total)
- **United States**: 700 universities
- **China**: 500 universities
- **India**: 500 universities
- **United Kingdom**: 300 universities
- **Germany**: 300 universities
- **Canada**: 300 universities
- **Plus 14 more countries**: France, Japan, Australia, Brazil, Italy, Spain, South Korea, Mexico, Switzerland, Sweden, Netherlands, South Africa, Singapore, Hong Kong

### Scholarships (4,011 total)
- **United States**: 805 scholarships
- **United Kingdom**: 503 scholarships
- **Canada**: 301 scholarships
- **Germany**: 301 scholarships
- **Australia**: 251 scholarships
- **Plus 13 more countries**: France (200), Japan (200), China (200), Netherlands (150), Sweden (150), Italy (150), Spain (150), Switzerland (100), India (100), Brazil (100), South Korea (100), Mexico (100), Singapore (50)

**Average Scholarship**: $27,959
**Maximum Scholarship**: $59,979
**Renewable**: 50.6%

---

## 🎨 Use Cases

### For Students
```bash
# Find your perfect match
curl -X POST "http://localhost:8000/api/search/combined" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "field": "Engineering",
    "level": "Undergraduate",
    "max_university_rank": 100,
    "min_scholarship_amount": 15000
  }'
```

### For Education Consultants
```bash
# Build comprehensive student profiles
# Get universities + scholarships in one call
# Export data for reports
```

### For Developers
```javascript
// Build education apps
// Integrate into admission platforms
// Create scholarship alert systems
// Build college comparison tools
```

### For Researchers
```bash
# Export complete datasets
curl http://localhost:8000/api/stats
# Analyze education trends
# Study scholarship distributions
```

---

## 🚀 Deployment

### Option 1: Render (Recommended)

1. **Push code to GitHub**
2. **Click Deploy to Render** button
3. **Set environment variables** (optional: OPENAI_API_KEY)
4. **Wait 10-15 minutes** for build (generates all data)
5. **Done!** Your platform is live

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Option 2: Other Platforms

The unified app can be deployed to:
- **Heroku**: `heroku create && git push heroku main`
- **Railway**: Connect GitHub repo
- **Fly.io**: `fly launch`
- **AWS/GCP/Azure**: Use Docker or direct deployment

---

## 🔍 Advanced Features

### Similarity Search
Uses KNN with cosine similarity to find similar institutions:
```python
# Algorithm: Content-based filtering
# Features: ranking, size, type, location, programs
# Model: K-Nearest Neighbors with PCA
# Performance: Sub-second response
```

### AI Chatbot (RAG)
Retrieval Augmented Generation for accurate responses:
```python
# Retrieval: TF-IDF vectorization
# Generation: OpenAI GPT-3.5-turbo
# Fallback: Rule-based responses without API key
# Context: Automatically determines universities vs scholarships
```

---

## 📈 Performance

- **Response Time**: < 500ms for most requests
- **Build Time**: 10-15 minutes (first deploy only)
- **Memory**: ~500MB RAM
- **Data Size**: ~5MB total
- **Concurrent Users**: Scales automatically on Render

---

## 🛠️ Development

### Run Tests
```bash
pytest tests/
```

### Generate Fresh Data
```bash
# Regenerate universities
python -m ai_native_playground.universities.generate_4000_data

# Regenerate scholarships
python -m ai_native_playground.scholarships.generate_scholarships
```

### Hot Reload (Development)
```bash
uvicorn ai_native_playground.education_platform.app:app --reload
```

---

## 🤝 API Examples Collection

### Example 1: Student Search
```bash
# High school senior looking for CS programs
curl -X POST "http://localhost:8000/api/search/combined" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "field": "Computer Science",
    "level": "Undergraduate",
    "max_university_rank": 50,
    "min_scholarship_amount": 20000,
    "scholarship_renewable": true,
    "n_universities": 15,
    "n_scholarships": 20
  }'
```

### Example 2: International Student
```bash
# Graduate student from India
curl -X POST "http://localhost:8000/api/search/combined" \
  -H "Content-Type: application/json" \
  -d '{
    "field": "Engineering",
    "level": "Graduate",
    "min_scholarship_amount": 25000,
    "n_universities": 20,
    "n_scholarships": 30
  }'
```

### Example 3: Conversational Search
```bash
# Natural language query
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to study medicine in the UK. What are my options for scholarships?"}'
```

---

## 💡 Tips & Tricks

1. **Start with Combined Search**: Get everything in one call
2. **Use Similar Search**: Found one you like? Find more like it
3. **Chat for Discovery**: Not sure what you want? Ask the AI
4. **Filter Strategically**: Combine filters for best results
5. **Check Stats First**: Understand what's available

---

## 🆘 Troubleshooting

**Problem**: Slow first request
- **Solution**: Free tier services sleep after inactivity. First request wakes them up (30-60s)

**Problem**: LLM responses are basic
- **Solution**: Set OPENAI_API_KEY for enhanced responses. Works fine without it though!

**Problem**: Build timeout on deployment
- **Solution**: Generating data takes time. Be patient, it's worth it!

**Problem**: No results found
- **Solution**: Try broader search criteria. Use `/api/stats` to see what's available.

---

## 📚 Related Documentation

- [Main README](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples

---

## 🎉 What's Next?

With the unified platform, you can:

1. **Build Student Apps**: Integrate into college planning tools
2. **Create Dashboards**: Visualize education data
3. **Automate Workflows**: Build scholarship alert systems
4. **Research Education**: Analyze trends and patterns
5. **Help Students**: Match students with perfect schools + funding

---

## 📞 Support

- **API Docs**: Visit `/api/docs` on your deployed URL
- **Issues**: Open on GitHub
- **Questions**: Check DEPLOYMENT.md and EXAMPLES.md

---

**Built with ❤️ using FastAPI, scikit-learn, and OpenAI**

Ready to deploy? Click the button at the top! 🚀
