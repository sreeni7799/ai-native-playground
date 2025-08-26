#!/usr/bin/env python3
"""Command-line interface for the Weather API."""

import uvicorn
from .main import app


def main():
    """Run the weather API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()