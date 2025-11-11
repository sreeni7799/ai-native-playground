"""
FastAPI application for University Recommendations and Chat
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from pathlib import Path

from .ml_model import UniversityRecommendationModel
from .llm_chat import UniversityChatbot

# Initialize FastAPI app
app = FastAPI(
    title="University Recommendation API",
    description="ML-powered university recommendations and LLM chatbot with 4,550+ universities",
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
        _ml_model = UniversityRecommendationModel()
        model_path = Path(__file__).parent / "data" / "university_recommendation_model_4k.pkl"
        if model_path.exists():
            _ml_model.load_model(str(model_path))
    return _ml_model


def get_chatbot():
    """Get or initialize chatbot."""
    global _chatbot
    if _chatbot is None:
        api_key = os.getenv('OPENAI_API_KEY')
        _chatbot = UniversityChatbot(api_key=api_key)
    return _chatbot


# Request/Response models
class RecommendationRequest(BaseModel):
    country: Optional[str] = None
    type: Optional[str] = None
    min_rank: Optional[int] = None
    max_rank: Optional[int] = None
    min_students: Optional[int] = None
    max_students: Optional[int] = None
    n_recommendations: int = 10


class SimilarRequest(BaseModel):
    university_name: str
    n_recommendations: int = 10


class ChatRequest(BaseModel):
    query: str


# API endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "University Recommendation API",
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
    Get university recommendations based on preferences.

    Example:
    ```json
    {
      "country": "United States",
      "type": "Private",
      "max_rank": 50,
      "n_recommendations": 10
    }
    ```
    """
    try:
        model = get_ml_model()

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

        results = model.recommend_by_preferences(
            preferences,
            n_recommendations=request.n_recommendations
        )

        return {
            "success": True,
            "count": len(results),
            "universities": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/similar")
async def find_similar(request: SimilarRequest):
    """
    Find universities similar to a given university.

    Example:
    ```json
    {
      "university_name": "Harvard University",
      "n_recommendations": 10
    }
    ```
    """
    try:
        model = get_ml_model()
        results = model.find_similar(
            request.university_name,
            n_recommendations=request.n_recommendations
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"University '{request.university_name}' not found"
            )

        return {
            "success": True,
            "query": request.university_name,
            "count": len(results),
            "universities": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI about universities.

    Example:
    ```json
    {
      "query": "Tell me about MIT"
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
            "universities_found": result['scholarships_found'],
            "using_llm": result['using_llm']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get database statistics."""
    try:
        model = get_ml_model()

        # Calculate statistics
        universities = model.universities

        countries = {}
        types = {}
        for uni in universities:
            country = uni.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1

            uni_type = uni.get('type', 'Unknown')
            types[uni_type] = types.get(uni_type, 0) + 1

        # Sort countries by count
        top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "success": True,
            "total_universities": len(universities),
            "countries": dict(top_countries),
            "types": types,
            "avg_ranking": sum(u.get('ranking', 0) for u in universities) / len(universities),
            "avg_students": sum(u.get('students', 0) for u in universities) / len(universities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
