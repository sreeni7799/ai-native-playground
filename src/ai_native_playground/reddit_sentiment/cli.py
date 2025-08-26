#!/usr/bin/env python3
"""Command-line interface for the Reddit Sentiment Analyzer."""

import uvicorn
from .main import app


def main():
    """Run the Reddit sentiment analyzer server."""
    print("🚀 Starting Reddit Sentiment Analyzer...")
    print("📊 Access the web interface at: http://localhost:8001")
    print("📖 API documentation at: http://localhost:8001/docs")
    print("⚠️  Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info"
    )


if __name__ == "__main__":
    main()