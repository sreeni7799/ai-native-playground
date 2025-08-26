from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any
import os
from pathlib import Path

from .reddit_client import RedditClient
from .sentiment_analyzer import SentimentAnalyzer

app = FastAPI(
    title="Reddit Sentiment Analyzer",
    description="Analyze the mood and sentiment of Reddit post comments",
    version="1.0.0"
)

# Get the directory of this file
current_dir = Path(__file__).parent

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(current_dir / "static")), name="static")
templates = Jinja2Templates(directory=str(current_dir / "templates"))

# Initialize components
reddit_client = RedditClient()
sentiment_analyzer = SentimentAnalyzer()


class RedditURLRequest(BaseModel):
    url: str
    max_comments: int = 100


class SentimentResponse(BaseModel):
    post_info: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    success: bool
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page with the Reddit URL form."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_model=SentimentResponse)
async def analyze_reddit_post(request: RedditURLRequest):
    """
    Analyze sentiment of Reddit post comments.
    
    Args:
        request: Contains Reddit URL and optional max_comments limit
        
    Returns:
        Sentiment analysis results including mood, confidence, and breakdown
    """
    try:
        # Validate Reddit URL
        if not reddit_client.validate_reddit_url(request.url):
            raise HTTPException(
                status_code=400, 
                detail="Invalid Reddit URL. Please provide a valid Reddit post URL."
            )
        
        # Fetch comments from Reddit
        reddit_data = reddit_client.fetch_post_comments(
            reddit_url=request.url,
            limit=min(request.max_comments, 500)  # Cap at 500 for performance
        )
        
        if not reddit_data['comments']:
            return SentimentResponse(
                post_info=reddit_data['post_info'],
                sentiment_analysis={
                    'overall_mood': 'neutral',
                    'confidence': 0.0,
                    'sentiment_distribution': {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0},
                    'mood_breakdown': {},
                    'total_comments': 0,
                    'message': 'No comments found for analysis'
                },
                success=True,
                message="Post found but no comments available for analysis"
            )
        
        # Analyze sentiment
        sentiment_results = sentiment_analyzer.analyze_comments_batch(reddit_data['comments'])
        
        return SentimentResponse(
            post_info=reddit_data['post_info'],
            sentiment_analysis=sentiment_results,
            success=True,
            message=f"Successfully analyzed {len(reddit_data['comments'])} comments"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing Reddit post: {str(e)}")


@app.post("/analyze-form")
async def analyze_reddit_post_form(
    request: Request,
    reddit_url: str = Form(...),
    max_comments: int = Form(100)
):
    """
    Handle form submission from the web interface.
    """
    try:
        # Create request object
        analysis_request = RedditURLRequest(url=reddit_url, max_comments=max_comments)
        
        # Validate Reddit URL
        if not reddit_client.validate_reddit_url(analysis_request.url):
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Invalid Reddit URL. Please provide a valid Reddit post URL.",
                    "reddit_url": reddit_url
                }
            )
        
        # Fetch and analyze
        reddit_data = reddit_client.fetch_post_comments(
            reddit_url=analysis_request.url,
            limit=min(analysis_request.max_comments, 500)
        )
        
        sentiment_results = sentiment_analyzer.analyze_comments_batch(reddit_data['comments'])
        
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "post_info": reddit_data['post_info'],
                "sentiment": sentiment_results,
                "reddit_url": reddit_url
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error analyzing Reddit post: {str(e)}",
                "reddit_url": reddit_url
            }
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Reddit Sentiment Analyzer"}


@app.get("/api/validate-url")
async def validate_reddit_url(url: str):
    """Validate if a URL is a valid Reddit post URL."""
    is_valid = reddit_client.validate_reddit_url(url)
    return {
        "url": url,
        "is_valid": is_valid,
        "message": "Valid Reddit URL" if is_valid else "Invalid Reddit URL format"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)