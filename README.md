# AI Native Playground

A collection of AI-powered Python applications including a weather API, news analyzer, and todo application. This repository demonstrates best practices for Python package structure, dependency management, and modular application design.

## 🚀 Features

### Weather API
- Get current weather for any city with enhanced data (UV index, feels like temperature)
- Get 8-day weather forecast for any city
- Uses OpenWeatherMap OneCall 3.0 API with geocoding
- Built with FastAPI and async/await patterns
- Comprehensive test coverage

### News Analyzer
- Fetch headlines from multiple news sources (Hacker News, Reddit, custom sites)
- AI-powered summarization and analysis of news content
- Support for multiple output formats
- Command-line interface with flexible options

### Todo Application
- Simple command-line todo management
- JSON-based persistence
- Add, list, and delete functionality

### Reddit Sentiment Analyzer
- Analyze mood and sentiment of Reddit post comments
- Web interface for easy Reddit URL submission
- Detailed sentiment breakdown with confidence scores
- Visual representation of positive/negative/neutral distribution
- No Reddit API key required - uses public JSON endpoints

## 📁 Project Structure

```
ai-native-playground/
├── src/
│   └── ai_native_playground/
│       ├── __init__.py
│       ├── weather_api/           # Weather API module
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── cli.py
│       ├── news_analyzer/         # News analysis module
│       │   ├── __init__.py
│       │   ├── news_agent.py
│       │   ├── news_orchestrator.py
│       │   ├── summarizer_agent.py
│       │   ├── demo.py
│       │   └── cli.py
│       ├── todo_app/              # Todo application module
│       │   ├── __init__.py
│       │   ├── todo.py
│       │   └── cli.py
│       ├── reddit_sentiment/      # Reddit sentiment analyzer module
│       │   ├── __init__.py
│       │   ├── reddit_client.py
│       │   ├── sentiment_analyzer.py
│       │   ├── main.py
│       │   ├── cli.py
│       │   ├── templates/         # HTML templates
│       │   └── static/            # CSS and JavaScript files
│       └── tests/                 # Test suite
│           ├── __init__.py
│           └── test_weather_api.py
├── requirements.txt               # Project dependencies
├── setup.py                      # Package installation script
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🛠️ Installation

### Option 1: Development Installation (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-native-playground

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

### Option 2: Production Installation
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Copy the environment variables template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

Get an API key from [OpenWeatherMap](https://openweathermap.org/api/one-call-3).

## 🎯 Usage

After installation, you can use the applications via command-line interfaces:

### Weather API
```bash
# Start the weather API server
weather-api

# The API will be available at http://localhost:8000
# Visit http://localhost:8000/docs for interactive documentation
```

### News Analyzer
```bash
# Analyze news from default sources
news-analyzer

# Analyze from specific sources with options
news-analyzer --sources https://news.ycombinator.com --max-headlines 20 --save

# Quick analysis mode
news-analyzer --quick
```

### Todo Application
```bash
# Add a new todo
todo-app add "Complete the project documentation"

# List all todos
todo-app list

# Delete a todo by ID
todo-app delete 1
```

### Reddit Sentiment Analyzer
```bash
# Start the web interface
reddit-sentiment

# The web app will be available at http://localhost:8001
# API documentation at http://localhost:8001/docs
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/ai_native_playground

# Run specific test file
pytest src/ai_native_playground/tests/test_weather_api.py -v
```

## 🔧 Development

### Code Quality Tools
```bash
# Format code with black
black src/

# Lint with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

### Project Structure Best Practices
- **Modular Design**: Each application is a separate module with clear boundaries
- **Package Structure**: Uses `src/` layout for better import handling
- **Entry Points**: Console scripts defined in `setup.py` for easy CLI access
- **Configuration**: Environment-based configuration with `.env` files
- **Testing**: Comprehensive test coverage with pytest
- **Documentation**: Clear README and inline documentation

## 🌐 API Endpoints (Weather API)

### Current Weather
```http
GET /current?city=London
```

### Weather Forecast
```http
GET /forecast?city=London
```

### Root Endpoint
```http
GET /
```

## 📝 Example Usage

### Weather API
```bash
# Get current weather
curl "http://localhost:8000/current?city=London"

# Get weather forecast
curl "http://localhost:8000/forecast?city=Tokyo"
```

### News Analyzer
```bash
# Basic usage
news-analyzer

# Advanced usage with custom sources
news-analyzer -s https://news.ycombinator.com https://www.reddit.com/r/technology -m 15 --save
```

### Reddit Sentiment Analyzer
```bash
# Example: Analyze a Reddit post via API
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/technology/comments/example/", "max_comments": 100}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- FastAPI for the excellent web framework
- BeautifulSoup for web scraping capabilities