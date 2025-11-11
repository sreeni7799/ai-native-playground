# 🚀 Deployment Guide - Render

Complete guide to deploy AI Native Playground on Render.com

## Table of Contents
- [Quick Deploy](#quick-deploy)
- [Services Overview](#services-overview)
- [Step-by-Step Deployment](#step-by-step-deployment)
- [Environment Variables](#environment-variables)
- [Testing Deployed Services](#testing-deployed-services)
- [Troubleshooting](#troubleshooting)
- [Cost Estimates](#cost-estimates)

---

## Quick Deploy

### Prerequisites
1. GitHub account with this repository
2. [Render account](https://render.com) (free tier available)
3. OpenWeatherMap API key (get from [openweathermap.org](https://openweathermap.org/api))
4. OpenAI API key (optional, for LLM features - get from [platform.openai.com](https://platform.openai.com))

### One-Click Deploy (Blueprint)

1. **Fork this repository** to your GitHub account

2. **Click the Deploy to Render button** (or follow manual steps below):

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

3. **Connect your GitHub** repository when prompted

4. **Set environment variables** in Render dashboard (see [Environment Variables](#environment-variables))

5. **Wait for build** (5-10 minutes for all services)

6. **Access your apps** via the provided URLs!

---

## Services Overview

This deployment includes **4 web services** (all can run on free tier):

### 1. Weather API 🌤️
**URL**: `https://ai-playground-weather-api.onrender.com`

**Features**:
- Current weather for any city
- 8-day weather forecast
- UV index, humidity, wind data

**Endpoints**:
- `GET /` - API info
- `GET /current?city=Boston` - Current weather
- `GET /forecast?city=Boston` - Forecast
- `GET /docs` - Interactive API docs

---

### 2. Reddit Sentiment Analyzer 😊
**URL**: `https://ai-playground-reddit-sentiment.onrender.com`

**Features**:
- Analyze sentiment of Reddit posts
- Web interface + REST API
- No Reddit API key required

**Endpoints**:
- `GET /` - Web interface
- `POST /analyze` - Analyze sentiment
- `GET /docs` - API documentation

---

### 3. University Recommendation API 🎓
**URL**: `https://ai-playground-university-api.onrender.com`

**Features**:
- ML-powered university recommendations
- 4,550 universities across 20 countries
- LLM chatbot with RAG (if OpenAI key provided)
- Find similar universities

**Endpoints**:
- `GET /` - API info
- `POST /api/recommend` - Get recommendations
- `POST /api/similar` - Find similar universities
- `POST /api/chat` - Chat about universities
- `GET /api/stats` - Database statistics
- `GET /docs` - Interactive API docs

---

### 4. Scholarship Recommendation API 💰
**URL**: `https://ai-playground-scholarship-api.onrender.com`

**Features**:
- ML-powered scholarship search
- 4,011 scholarships across 18 countries
- LLM chatbot for natural language queries
- Filter by country, field, amount, etc.

**Endpoints**:
- `GET /` - API info
- `POST /api/recommend` - Get recommendations
- `POST /api/similar` - Find similar scholarships
- `POST /api/chat` - Chat about scholarships
- `GET /api/stats` - Database statistics
- `GET /docs` - Interactive API docs

---

## Step-by-Step Deployment

### Method 1: Using Blueprint (render.yaml)

**Easiest method** - Deploys all services at once.

1. **Push to GitHub**:
   ```bash
   git add render.yaml
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Go to Render Dashboard**:
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New"** → **"Blueprint"**

3. **Connect Repository**:
   - Select your GitHub repository
   - Render will detect `render.yaml`
   - Click **"Apply"**

4. **Set Environment Variables** (see section below)

5. **Deploy**:
   - Render will build and deploy all services
   - First build takes 5-10 minutes
   - Subsequent builds are faster

---

### Method 2: Manual Deployment (Individual Services)

Deploy each service one by one for more control.

#### Deploy Weather API

1. **Create New Web Service**:
   - Go to Render Dashboard
   - Click **"New"** → **"Web Service"**
   - Connect your GitHub repository

2. **Configure**:
   ```
   Name: ai-playground-weather-api
   Environment: Python 3
   Region: Oregon (or closest to you)
   Branch: main
   Build Command: pip install -e .
   Start Command: uvicorn ai_native_playground.weather_api.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   - Add `OPENWEATHER_API_KEY` (required)
   - Add `PYTHON_VERSION=3.11.0`

4. **Deploy**: Click **"Create Web Service"**

#### Deploy Reddit Sentiment

1. **Create New Web Service**

2. **Configure**:
   ```
   Name: ai-playground-reddit-sentiment
   Environment: Python 3
   Build Command: pip install -e .
   Start Command: uvicorn ai_native_playground.reddit_sentiment.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Deploy**

#### Deploy University API

1. **Create New Web Service**

2. **Configure**:
   ```
   Name: ai-playground-university-api
   Environment: Python 3
   Build Command: pip install -e . && python -m ai_native_playground.universities.generate_4000_data
   Start Command: uvicorn ai_native_playground.universities.api:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   - Add `OPENAI_API_KEY` (optional, for LLM features)
   - Add `PYTHON_VERSION=3.11.0`

4. **Deploy**

**Note**: First build takes longer (~5-10 min) to generate university data.

#### Deploy Scholarship API

1. **Create New Web Service**

2. **Configure**:
   ```
   Name: ai-playground-scholarship-api
   Environment: Python 3
   Build Command: pip install -e . && python -m ai_native_playground.scholarships.generate_scholarships
   Start Command: uvicorn ai_native_playground.scholarships.api:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   - Add `OPENAI_API_KEY` (optional)
   - Add `PYTHON_VERSION=3.11.0`

4. **Deploy**

---

## Environment Variables

Set these in the Render Dashboard for each service:

### Weather API (Required)
```env
OPENWEATHER_API_KEY=your_api_key_here
PYTHON_VERSION=3.11.0
```

**Get API Key**:
1. Visit [openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for free account
3. Get API key from dashboard

### University & Scholarship APIs (Optional)
```env
OPENAI_API_KEY=your_openai_api_key_here
PYTHON_VERSION=3.11.0
```

**Get API Key**:
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account
3. Generate API key
4. Add billing (pay-as-you-go)

**Note**: Without OpenAI key, LLM chat features will use fallback mode (still functional).

---

## Testing Deployed Services

### Test Weather API
```bash
# Get current weather
curl "https://your-app.onrender.com/current?city=Boston"

# Get forecast
curl "https://your-app.onrender.com/forecast?city=London"

# View interactive docs
open "https://your-app.onrender.com/docs"
```

**Expected Response**:
```json
{
  "city": "Boston",
  "temperature": 72.5,
  "feels_like": 70.3,
  "weather_main": "Clear",
  "humidity": 65,
  ...
}
```

---

### Test Reddit Sentiment
```bash
# Visit web interface
open "https://your-app.onrender.com"

# Or use API
curl -X POST "https://your-app.onrender.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/technology/comments/xyz/", "max_comments": 100}'
```

---

### Test University API
```bash
# Get recommendations
curl -X POST "https://your-app.onrender.com/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"country": "United States", "max_rank": 50, "n_recommendations": 10}'

# Find similar universities
curl -X POST "https://your-app.onrender.com/api/similar" \
  -H "Content-Type: application/json" \
  -d '{"university_name": "Harvard University", "n_recommendations": 10}'

# Chat with AI
curl -X POST "https://your-app.onrender.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about MIT"}'

# Get statistics
curl "https://your-app.onrender.com/api/stats"

# Interactive docs
open "https://your-app.onrender.com/docs"
```

---

### Test Scholarship API
```bash
# Get recommendations
curl -X POST "https://your-app.onrender.com/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"country": "United States", "field": "Engineering", "min_amount": 20000, "n_recommendations": 10}'

# Find similar scholarships
curl -X POST "https://your-app.onrender.com/api/similar" \
  -H "Content-Type: application/json" \
  -d '{"scholarship_name": "Fulbright Program", "n_recommendations": 10}'

# Chat about scholarships
curl -X POST "https://your-app.onrender.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me engineering scholarships"}'

# Get statistics
curl "https://your-app.onrender.com/api/stats"

# Interactive docs
open "https://your-app.onrender.com/docs"
```

---

## Frontend Integration

### JavaScript/React Example

```javascript
// University API
const API_BASE = 'https://your-university-api.onrender.com';

// Get recommendations
async function getUniversityRecommendations(preferences) {
  const response = await fetch(`${API_BASE}/api/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(preferences)
  });
  return await response.json();
}

// Example usage
const recommendations = await getUniversityRecommendations({
  country: "United States",
  max_rank: 50,
  n_recommendations: 10
});

console.log(recommendations.universities);
```

```javascript
// Scholarship API
const SCHOLARSHIP_API = 'https://your-scholarship-api.onrender.com';

async function findScholarships(criteria) {
  const response = await fetch(`${SCHOLARSHIP_API}/api/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(criteria)
  });
  return await response.json();
}

// Example
const scholarships = await findScholarships({
  country: "United States",
  field: "Computer Science",
  level: "Graduate",
  min_amount: 25000,
  renewable: true,
  n_recommendations: 20
});
```

---

## Troubleshooting

### Issue: Build Fails

**Symptom**: Build fails with dependency errors

**Solutions**:
1. Check Python version:
   ```env
   PYTHON_VERSION=3.11.0
   ```

2. Verify `requirements.txt` is up to date

3. Check build logs in Render dashboard

---

### Issue: Service Times Out

**Symptom**: "Service Unavailable" or timeouts

**Solutions**:
1. **Free tier services sleep after 15 min of inactivity**
   - First request after sleep takes 30-60 seconds
   - Upgrade to paid plan for always-on service

2. **Build timeout** (for university/scholarship APIs):
   - Generating data takes time on first build
   - Be patient, takes 5-10 minutes
   - Check logs for progress

---

### Issue: LLM Features Not Working

**Symptom**: Chat returns basic responses

**Solutions**:
1. Verify `OPENAI_API_KEY` is set correctly
2. Check OpenAI account has credits
3. LLM features degrade gracefully - will work without key, just less sophisticated

---

### Issue: Large Data Files

**Symptom**: Deployment fails due to file size

**Solutions**:
1. University/scholarship data generated during build
2. Models (~3MB) are included in repo
3. If issues, check `.gitignore` isn't excluding data files

---

### Issue: CORS Errors (Frontend)

**Symptom**: Browser blocks API requests

**Solutions**:
- All APIs have CORS enabled by default
- If issues, check browser console for specific error
- Verify request format matches API docs

---

## Cost Estimates

### Free Tier (All Services)
- **Cost**: $0/month
- **Limitations**:
  - Services sleep after 15 min inactivity
  - 750 hours/month per service (enough for light use)
  - Shared resources

**Recommended for**:
- Testing and development
- Personal projects
- Low-traffic applications

---

### Starter Plan ($7/month per service)
- **Cost**: $28/month for 4 services
- **Benefits**:
  - Services always on (no sleep)
  - Better performance
  - More resources

**Recommended for**:
- Production apps
- Moderate traffic
- Business use

---

### API Usage Costs

**OpenWeatherMap**:
- Free tier: 1,000 calls/day
- Cost: $0 for personal use

**OpenAI (for LLM features)**:
- GPT-3.5-turbo: ~$0.002 per chat query
- 1,000 queries ≈ $2
- Optional - fallback mode works without it

---

## Monitoring & Maintenance

### View Logs
1. Go to Render Dashboard
2. Select service
3. Click **"Logs"** tab
4. Real-time logs shown

### Monitor Performance
- Render dashboard shows:
  - CPU usage
  - Memory usage
  - Request counts
  - Error rates

### Auto-Deploy
- Render auto-deploys on git push to main branch
- Disable in service settings if needed

---

## Advanced Configuration

### Custom Domain
1. Go to service settings
2. Click **"Custom Domain"**
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS records as shown

### Environment-Specific Configs
```yaml
# render.yaml
services:
  - type: web
    name: my-api
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
```

### Database (if needed)
```yaml
databases:
  - name: my-postgres-db
    databaseName: mydb
    user: myuser
```

---

## Scaling Tips

### Optimize Build Time
1. **Cache dependencies**:
   - Render caches pip installs
   - Don't regenerate data every build

2. **Pre-build data**:
   ```bash
   # Run locally, commit generated files
   python -m ai_native_playground.universities.generate_4000_data
   git add src/ai_native_playground/universities/data/
   git commit -m "Add pre-generated data"
   ```

### Improve Response Time
1. **Use caching**:
   - Add Redis for frequent queries
   - Cache ML model predictions

2. **Optimize models**:
   - Reduce dataset size if needed
   - Use smaller ML models

3. **CDN for static files**:
   - Host static assets on CDN
   - Serve from edge locations

---

## Alternative Deployment Options

### Other Platforms

**Heroku**:
- Similar to Render
- More expensive
- Better documentation

**Railway**:
- Developer-friendly
- Good free tier
- Simpler UI

**Fly.io**:
- Edge deployment
- Better global performance
- More complex setup

**AWS/GCP/Azure**:
- Most powerful
- Most expensive
- Requires more configuration

---

## Support & Resources

**Render Documentation**:
- [docs.render.com](https://docs.render.com)

**This Project**:
- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [EXAMPLES.md](EXAMPLES.md) - Use case examples

**Get Help**:
- Open issue on GitHub
- Check Render community forum
- Email support@render.com

---

## Checklist

Before deploying, make sure you have:

- [ ] Forked/cloned repository
- [ ] Obtained OpenWeatherMap API key
- [ ] (Optional) Obtained OpenAI API key
- [ ] Created Render account
- [ ] Reviewed `render.yaml` configuration
- [ ] Set up environment variables
- [ ] Tested locally first (recommended)
- [ ] Committed latest changes to GitHub
- [ ] Read deployment guide

After deploying:

- [ ] Verified all services started successfully
- [ ] Tested each API endpoint
- [ ] Checked logs for errors
- [ ] Set up custom domains (if needed)
- [ ] Configured monitoring
- [ ] Documented your API URLs

---

**Happy Deploying! 🚀**

Need help? Open an issue or check the [troubleshooting section](#troubleshooting).
