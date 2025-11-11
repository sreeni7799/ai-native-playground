"""
FastAPI application for Scholarship Recommendations and Chat
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from pathlib import Path

from .ml_model import ScholarshipRecommendationModel
from .llm_chat import ScholarshipChatbot

# Initialize FastAPI app
app = FastAPI(
    title="Scholarship Recommendation API",
    description="ML-powered scholarship recommendations and LLM chatbot with 4,000+ scholarships",
    version="1.0.0"
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
_ml_model = None
_chatbot = None


def get_ml_model():
    """Get or initialize ML model."""
    global _ml_model
    if _ml_model is None:
        _ml_model = ScholarshipRecommendationModel()
        model_path = Path(__file__).parent / "data" / "scholarship_recommendation_model.pkl"
        if model_path.exists():
            _ml_model.load_model(str(model_path))
    return _ml_model


def get_chatbot():
    """Get or initialize chatbot."""
    global _chatbot
    if _chatbot is None:
        api_key = os.getenv('OPENAI_API_KEY')
        _chatbot = ScholarshipChatbot(api_key=api_key)
    return _chatbot


# Request/Response models
class RecommendationRequest(BaseModel):
    country: Optional[str] = None
    field: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None
    renewable: Optional[bool] = None
    n_recommendations: int = 10


class SimilarRequest(BaseModel):
    scholarship_name: str
    n_recommendations: int = 10


class ChatRequest(BaseModel):
    query: str


# API endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Scholarship Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "recommendations": "/api/recommend",
            "similar": "/api/similar",
            "chat": "/api/chat",
            "stats": "/api/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/recommend")
async def get_recommendations(request: RecommendationRequest):
    """
    Get scholarship recommendations based on preferences.

    Example:
    ```json
    {
      "country": "United States",
      "field": "Computer Science",
      "level": "Graduate",
      "min_amount": 20000,
      "renewable": true,
      "n_recommendations": 10
    }
    ```
    """
    try:
        model = get_ml_model()

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

        results = model.recommend_by_preferences(
            preferences,
            n_recommendations=request.n_recommendations
        )

        return {
            "success": True,
            "count": len(results),
            "scholarships": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/similar")
async def find_similar(request: SimilarRequest):
    """
    Find scholarships similar to a given scholarship.

    Example:
    ```json
    {
      "scholarship_name": "Fulbright Program",
      "n_recommendations": 10
    }
    ```
    """
    try:
        model = get_ml_model()
        results = model.find_similar(
            request.scholarship_name,
            n_recommendations=request.n_recommendations
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Scholarship '{request.scholarship_name}' not found"
            )

        return {
            "success": True,
            "query": request.scholarship_name,
            "count": len(results),
            "scholarships": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI about scholarships.

    Example:
    ```json
    {
      "query": "Show me engineering scholarships"
    }
    ```
    """
    try:
        chatbot = get_chatbot()
        result = chatbot.chat(request.query)

        return {
            "success": True,
            "query": request.query,
            "response": result['response'],
            "scholarships_found": result['scholarships_found'],
            "using_llm": result['using_llm']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get database statistics."""
    try:
        model = get_ml_model()
        scholarships = model.scholarships

        # Calculate statistics
        countries = {}
        fields = {}
        levels = {}
        types = {}

        for s in scholarships:
            country = s.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1

            field = s.get('field', 'Unknown')
            fields[field] = fields.get(field, 0) + 1

            level = s.get('level', 'Unknown')
            levels[level] = levels.get(level, 0) + 1

            s_type = s.get('type', 'Unknown')
            types[s_type] = types.get(s_type, 0) + 1

        # Sort by count
        top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]
        top_fields = sorted(fields.items(), key=lambda x: x[1], reverse=True)[:10]

        amounts = [s.get('amount', 0) for s in scholarships]
        renewable_count = sum(1 for s in scholarships if s.get('renewable'))

        return {
            "success": True,
            "total_scholarships": len(scholarships),
            "countries": dict(top_countries),
            "fields": dict(top_fields),
            "levels": levels,
            "types": dict(sorted(types.items(), key=lambda x: x[1], reverse=True)[:10]),
            "avg_amount": sum(amounts) / len(amounts) if amounts else 0,
            "max_amount": max(amounts) if amounts else 0,
            "renewable_count": renewable_count,
            "renewable_percentage": (renewable_count / len(scholarships) * 100) if scholarships else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
