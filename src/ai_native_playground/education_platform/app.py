"""
Unified Education Platform API

Combines University Recommendations (4,550 universities) and
Scholarship Search (4,011 scholarships) into one powerful platform.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from pathlib import Path

# Import university components
from ..universities.ml_model import UniversityRecommendationModel
from ..universities.llm_chat import UniversityChatbot

# Import scholarship components
from ..scholarships.ml_model import ScholarshipRecommendationModel
from ..scholarships.llm_chat import ScholarshipChatbot

# Initialize FastAPI app
app = FastAPI(
    title="AI Education Platform",
    description="Complete education search platform with 4,550+ universities and 4,011+ scholarships. ML recommendations + AI chatbot powered.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models (lazy loading)
_university_model = None
_scholarship_model = None
_university_chatbot = None
_scholarship_chatbot = None


def get_university_model():
    """Get or initialize university ML model."""
    global _university_model
    if _university_model is None:
        _university_model = UniversityRecommendationModel()
        model_path = Path(__file__).parent.parent / "universities" / "data" / "university_recommendation_model_4k.pkl"
        if model_path.exists():
            _university_model.load_model(str(model_path))
    return _university_model


def get_scholarship_model():
    """Get or initialize scholarship ML model."""
    global _scholarship_model
    if _scholarship_model is None:
        _scholarship_model = ScholarshipRecommendationModel()
        model_path = Path(__file__).parent.parent / "scholarships" / "data" / "scholarship_recommendation_model.pkl"
        if model_path.exists():
            _scholarship_model.load_model(str(model_path))
    return _scholarship_model


def get_university_chatbot():
    """Get or initialize university chatbot."""
    global _university_chatbot
    if _university_chatbot is None:
        api_key = os.getenv('OPENAI_API_KEY')
        _university_chatbot = UniversityChatbot(api_key=api_key)
    return _university_chatbot


def get_scholarship_chatbot():
    """Get or initialize scholarship chatbot."""
    global _scholarship_chatbot
    if _scholarship_chatbot is None:
        api_key = os.getenv('OPENAI_API_KEY')
        _scholarship_chatbot = ScholarshipChatbot(api_key=api_key)
    return _scholarship_chatbot


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UniversityRecommendRequest(BaseModel):
    country: Optional[str] = None
    type: Optional[str] = None
    min_rank: Optional[int] = None
    max_rank: Optional[int] = None
    min_students: Optional[int] = None
    max_students: Optional[int] = None
    n_recommendations: int = 10


class ScholarshipRecommendRequest(BaseModel):
    country: Optional[str] = None
    field: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None
    renewable: Optional[bool] = None
    n_recommendations: int = 10


class CombinedSearchRequest(BaseModel):
    """Search for both universities and scholarships at once."""
    country: Optional[str] = None
    field: Optional[str] = None
    level: Optional[str] = "Undergraduate"
    max_university_rank: Optional[int] = None
    min_scholarship_amount: Optional[int] = None
    scholarship_renewable: Optional[bool] = None
    n_universities: int = 10
    n_scholarships: int = 10


class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = "general"  # "general", "universities", "scholarships"


class SimilarRequest(BaseModel):
    name: str
    n_recommendations: int = 10


# ============================================================================
# ROOT & INFO ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    html_path = Path(__file__).parent / "templates" / "index.html"
    if html_path.exists():
        with open(html_path, 'r') as f:
            return f.read()

    # Fallback HTML
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Education Platform</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }
            .container {
                background: white;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
            }
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            .endpoints {
                background: #f7fafc;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .endpoint {
                background: white;
                padding: 12px;
                margin: 8px 0;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }
            .method {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 0.85em;
                font-weight: bold;
                margin-right: 10px;
            }
            .button {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                text-decoration: none;
                margin: 10px 10px 10px 0;
                transition: transform 0.2s;
            }
            .button:hover {
                transform: translateY(-2px);
                background: #5568d3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 AI Education Platform</h1>
            <p style="font-size: 1.2em; color: #666;">
                Complete education search platform powered by Machine Learning and AI
            </p>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">4,550</div>
                    <div class="stat-label">Universities Worldwide</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">4,011</div>
                    <div class="stat-label">Scholarships Available</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">20</div>
                    <div class="stat-label">Countries Covered</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">AI</div>
                    <div class="stat-label">Powered Chatbot</div>
                </div>
            </div>

            <h2>🚀 Quick Start</h2>
            <a href="/api/docs" class="button">📚 Interactive API Docs</a>
            <a href="/api/stats" class="button">📊 View Statistics</a>
            <a href="/health" class="button">❤️ Health Check</a>

            <div class="endpoints">
                <h3>🎯 Main Endpoints</h3>

                <div class="endpoint">
                    <span class="method">POST</span>
                    <strong>/api/search/combined</strong> - Search universities & scholarships together
                </div>

                <div class="endpoint">
                    <span class="method">POST</span>
                    <strong>/api/universities/recommend</strong> - Get university recommendations
                </div>

                <div class="endpoint">
                    <span class="method">POST</span>
                    <strong>/api/scholarships/recommend</strong> - Get scholarship recommendations
                </div>

                <div class="endpoint">
                    <span class="method">POST</span>
                    <strong>/api/chat</strong> - Chat with AI about education
                </div>

                <div class="endpoint">
                    <span class="method">GET</span>
                    <strong>/api/stats</strong> - Get complete platform statistics
                </div>
            </div>

            <h2>💡 Features</h2>
            <ul style="font-size: 1.1em; line-height: 1.8;">
                <li>🤖 <strong>ML-Powered Recommendations</strong> - Content-based filtering with KNN</li>
                <li>💬 <strong>AI Chatbot</strong> - Natural language queries with RAG system</li>
                <li>🔍 <strong>Combined Search</strong> - Find universities and scholarships in one query</li>
                <li>🌍 <strong>Global Coverage</strong> - 20 countries, 18 scholarship regions</li>
                <li>🎓 <strong>Comprehensive Data</strong> - Rankings, programs, amounts, eligibility</li>
                <li>⚡ <strong>Fast API</strong> - Sub-second response times</li>
            </ul>

            <h2>📖 Example Usage</h2>
            <pre style="background: #f7fafc; padding: 20px; border-radius: 8px; overflow-x: auto;">
# Combined search for universities + scholarships
curl -X POST "https://your-app.onrender.com/api/search/combined" \\
  -H "Content-Type: application/json" \\
  -d '{
    "country": "United States",
    "field": "Computer Science",
    "max_university_rank": 50,
    "min_scholarship_amount": 20000,
    "n_universities": 10,
    "n_scholarships": 10
  }'

# Chat with AI
curl -X POST "https://your-app.onrender.com/api/chat" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What are good engineering schools with scholarships?"}'
            </pre>

            <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #666;">
                <p>Built with FastAPI, scikit-learn, and OpenAI | <a href="https://github.com/yourusername/ai-native-playground" style="color: #667eea;">View on GitHub</a></p>
            </footer>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "universities": "operational",
            "scholarships": "operational",
            "ml_models": "loaded",
            "llm_chatbot": "available" if os.getenv('OPENAI_API_KEY') else "fallback_mode"
        }
    }


@app.get("/api/stats")
async def get_platform_stats():
    """Get complete platform statistics."""
    try:
        uni_model = get_university_model()
        scholarship_model = get_scholarship_model()

        universities = uni_model.universities
        scholarships = scholarship_model.scholarships

        # University stats
        uni_countries = {}
        uni_types = {}
        for uni in universities:
            country = uni.get('country', 'Unknown')
            uni_countries[country] = uni_countries.get(country, 0) + 1
            uni_type = uni.get('type', 'Unknown')
            uni_types[uni_type] = uni_types.get(uni_type, 0) + 1

        # Scholarship stats
        scholarship_countries = {}
        scholarship_fields = {}
        for s in scholarships:
            country = s.get('country', 'Unknown')
            scholarship_countries[country] = scholarship_countries.get(country, 0) + 1
            field = s.get('field', 'Unknown')
            scholarship_fields[field] = scholarship_fields.get(field, 0) + 1

        amounts = [s.get('amount', 0) for s in scholarships]
        renewable_count = sum(1 for s in scholarships if s.get('renewable'))

        return {
            "success": True,
            "platform": {
                "version": "2.0.0",
                "total_universities": len(universities),
                "total_scholarships": len(scholarships),
                "total_countries": len(set(list(uni_countries.keys()) + list(scholarship_countries.keys())))
            },
            "universities": {
                "total": len(universities),
                "countries": dict(sorted(uni_countries.items(), key=lambda x: x[1], reverse=True)[:10]),
                "types": uni_types,
                "avg_ranking": sum(u.get('ranking', 0) for u in universities) / len(universities),
                "avg_students": sum(u.get('students', 0) for u in universities) / len(universities)
            },
            "scholarships": {
                "total": len(scholarships),
                "countries": dict(sorted(scholarship_countries.items(), key=lambda x: x[1], reverse=True)[:10]),
                "top_fields": dict(sorted(scholarship_fields.items(), key=lambda x: x[1], reverse=True)[:10]),
                "avg_amount": sum(amounts) / len(amounts) if amounts else 0,
                "max_amount": max(amounts) if amounts else 0,
                "renewable_count": renewable_count,
                "renewable_percentage": (renewable_count / len(scholarships) * 100) if scholarships else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# COMBINED SEARCH ENDPOINT (THE POWER FEATURE!)
# ============================================================================

@app.post("/api/search/combined")
async def combined_search(request: CombinedSearchRequest):
    """
    🔥 POWER FEATURE: Search for universities AND scholarships in one query!

    Perfect for students who want to find schools and funding opportunities together.

    Example:
    ```json
    {
      "country": "United States",
      "field": "Computer Science",
      "level": "Undergraduate",
      "max_university_rank": 50,
      "min_scholarship_amount": 20000,
      "scholarship_renewable": true,
      "n_universities": 10,
      "n_scholarships": 10
    }
    ```
    """
    try:
        uni_model = get_university_model()
        scholarship_model = get_scholarship_model()

        # Build university preferences
        uni_prefs = {}
        if request.country:
            uni_prefs['country'] = request.country
        if request.max_university_rank:
            uni_prefs['max_rank'] = request.max_university_rank

        # Build scholarship preferences
        scholarship_prefs = {}
        if request.country:
            scholarship_prefs['country'] = request.country
        if request.field:
            scholarship_prefs['field'] = request.field
        if request.level:
            scholarship_prefs['level'] = request.level
        if request.min_scholarship_amount:
            scholarship_prefs['min_amount'] = request.min_scholarship_amount
        if request.scholarship_renewable is not None:
            scholarship_prefs['renewable'] = request.scholarship_renewable

        # Get recommendations
        universities = uni_model.recommend_by_preferences(uni_prefs, n_recommendations=request.n_universities)
        scholarships = scholarship_model.recommend_by_preferences(scholarship_prefs, n_recommendations=request.n_scholarships)

        # Calculate combined statistics
        total_scholarship_value = sum(s['amount'] for s in scholarships)
        renewable_scholarships = sum(1 for s in scholarships if s.get('renewable'))

        return {
            "success": True,
            "search_criteria": {
                "country": request.country,
                "field": request.field,
                "level": request.level
            },
            "universities": {
                "count": len(universities),
                "results": universities,
                "avg_ranking": sum(u['ranking'] for u in universities) / len(universities) if universities else 0
            },
            "scholarships": {
                "count": len(scholarships),
                "results": scholarships,
                "total_value": total_scholarship_value,
                "avg_amount": total_scholarship_value / len(scholarships) if scholarships else 0,
                "renewable_count": renewable_scholarships
            },
            "summary": {
                "total_results": len(universities) + len(scholarships),
                "potential_funding": f"${total_scholarship_value:,}",
                "recommendation": f"Apply to {len(universities)} universities with ${total_scholarship_value:,} in potential scholarships"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UNIVERSITY ENDPOINTS
# ============================================================================

@app.post("/api/universities/recommend")
async def recommend_universities(request: UniversityRecommendRequest):
    """Get university recommendations based on preferences."""
    try:
        model = get_university_model()

        preferences = {}
        if request.country:
            preferences['country'] = request.country
        if request.type:
            preferences['type'] = request.type
        if request.min_rank:
            preferences['min_rank'] = request.min_rank
        if request.max_rank:
            preferences['max_rank'] = request.max_rank
        if request.min_students:
            preferences['min_students'] = request.min_students
        if request.max_students:
            preferences['max_students'] = request.max_students

        results = model.recommend_by_preferences(preferences, n_recommendations=request.n_recommendations)

        return {
            "success": True,
            "count": len(results),
            "universities": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/universities/similar")
async def find_similar_universities(request: SimilarRequest):
    """Find universities similar to a given university."""
    try:
        model = get_university_model()
        results = model.find_similar(request.name, n_recommendations=request.n_recommendations)

        if not results:
            raise HTTPException(status_code=404, detail=f"University '{request.name}' not found")

        return {
            "success": True,
            "query": request.name,
            "count": len(results),
            "universities": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SCHOLARSHIP ENDPOINTS
# ============================================================================

@app.post("/api/scholarships/recommend")
async def recommend_scholarships(request: ScholarshipRecommendRequest):
    """Get scholarship recommendations based on preferences."""
    try:
        model = get_scholarship_model()

        preferences = {}
        if request.country:
            preferences['country'] = request.country
        if request.field:
            preferences['field'] = request.field
        if request.level:
            preferences['level'] = request.level
        if request.type:
            preferences['type'] = request.type
        if request.min_amount:
            preferences['min_amount'] = request.min_amount
        if request.max_amount:
            preferences['max_amount'] = request.max_amount
        if request.renewable is not None:
            preferences['renewable'] = request.renewable

        results = model.recommend_by_preferences(preferences, n_recommendations=request.n_recommendations)

        return {
            "success": True,
            "count": len(results),
            "scholarships": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scholarships/similar")
async def find_similar_scholarships(request: SimilarRequest):
    """Find scholarships similar to a given scholarship."""
    try:
        model = get_scholarship_model()
        results = model.find_similar(request.name, n_recommendations=request.n_recommendations)

        if not results:
            raise HTTPException(status_code=404, detail=f"Scholarship '{request.name}' not found")

        return {
            "success": True,
            "query": request.name,
            "count": len(results),
            "scholarships": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AI CHATBOT ENDPOINT
# ============================================================================

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI about universities, scholarships, or both!

    The AI will automatically determine if you're asking about universities,
    scholarships, or both, and provide relevant information.

    Example queries:
    - "What are good engineering schools with scholarships?"
    - "Tell me about MIT"
    - "Show me renewable scholarships over $30,000"
    - "Compare Stanford and Harvard"
    """
    try:
        query_lower = request.query.lower()

        # Determine context if not specified
        if request.context == "general":
            if any(word in query_lower for word in ['scholarship', 'funding', 'financial aid', 'grant']):
                context = "scholarships"
            elif any(word in query_lower for word in ['university', 'college', 'school', 'program']):
                context = "universities"
            else:
                # Default to combined response
                context = "both"
        else:
            context = request.context

        responses = []

        # Get university response
        if context in ["universities", "both"]:
            uni_chatbot = get_university_chatbot()
            uni_result = uni_chatbot.chat(request.query)
            responses.append({
                "type": "universities",
                "response": uni_result['response'],
                "items_found": uni_result.get('scholarships_found', 0),
                "using_llm": uni_result['using_llm']
            })

        # Get scholarship response
        if context in ["scholarships", "both"]:
            scholarship_chatbot = get_scholarship_chatbot()
            scholarship_result = scholarship_chatbot.chat(request.query)
            responses.append({
                "type": "scholarships",
                "response": scholarship_result['response'],
                "items_found": scholarship_result['scholarships_found'],
                "using_llm": scholarship_result['using_llm']
            })

        # Combine responses if both
        if context == "both" and len(responses) == 2:
            combined_response = f"🎓 UNIVERSITIES:\n{responses[0]['response']}\n\n💰 SCHOLARSHIPS:\n{responses[1]['response']}"
            return {
                "success": True,
                "query": request.query,
                "context": "combined",
                "response": combined_response,
                "universities_found": responses[0]['items_found'],
                "scholarships_found": responses[1]['items_found'],
                "using_llm": responses[0]['using_llm'] or responses[1]['using_llm']
            }
        else:
            resp = responses[0]
            return {
                "success": True,
                "query": request.query,
                "context": resp['type'],
                "response": resp['response'],
                "items_found": resp['items_found'],
                "using_llm": resp['using_llm']
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
