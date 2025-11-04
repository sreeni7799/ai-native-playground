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

### German Universities Data Scraper
- Comprehensive data for top 10 universities in Germany
- Includes location, founding year, student population, and rankings
- Faculty information and notable programs
- Export data to JSON format for model training
- Summary statistics and formatted display

### 🌍 Global Universities Dataset (4,550 Universities!)
- Comprehensive dataset of **4,550 universities across 20 countries**
- **United States**: 700 universities
- **China**: 500 universities
- **India**: 500 universities
- **Canada**: 300 universities
- **Germany**: 300 universities
- **United Kingdom**: 300 universities
- **France**: 250 universities
- **Japan**: 200 universities
- **Australia**: 200 universities
- **Brazil**: 200 universities
- Plus: Italy (150), Spain (150), South Korea (150), Mexico (150), Switzerland (100), Sweden (100), Netherlands (100), South Africa (100), Singapore (50), Hong Kong (50)
- Includes rankings, student populations, founding years, and notable programs
- CLI for searching, filtering, and exporting data
- Perfect for AI/ML model training and research

### 🤖 ML-Powered University Recommendation System
- **Trained machine learning model** using scikit-learn on **4,550 universities**
- **Content-based filtering** using university features (ranking, size, type, location)
- **Similarity search** to find universities similar to your favorites
- **Personalized recommendations** based on your preferences
- Features: K-Nearest Neighbors, PCA dimensionality reduction, cosine similarity
- Trained model size: ~3MB, fast inference (<1 second)
- Command-line interface for instant recommendations
- Global coverage: 20 countries across 6 continents

### 💬 LLM-Powered University Chatbot (RAG System)
- **Chat naturally** with an AI about universities using OpenAI GPT
- **Retrieval Augmented Generation (RAG)** - Answers backed by real data
- **4,550 university database** across 20 countries as knowledge base
- **Interactive CLI** for conversational queries
- Ask about universities in US, China, India, UK, Germany, Japan, and 14 more countries
- Works with or without OpenAI API key (fallback mode available)

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
│       ├── german_universities/   # German universities scraper module
│       │   ├── __init__.py
│       │   ├── scraper.py
│       │   ├── cli.py
│       │   └── data/              # Output data directory
│       ├── universities/          # Global universities dataset (1000+)
│       │   ├── __init__.py
│       │   ├── data_loader.py
│       │   ├── generate_data.py
│       │   ├── cli.py
│       │   └── data/              # Dataset storage
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

### German Universities Data Scraper
```bash
# Display all universities with details
german-universities

# Save data to JSON file
german-universities --save

# Show only summary statistics
german-universities --stats-only

# Custom output filename
german-universities --save --output my_universities.json
```

### Global Universities Dataset
```bash
# Show comprehensive statistics
universities --stats

# List universities from a specific country
universities --country "United States" --limit 20
universities --country Canada --limit 15
universities --country Germany

# Search for universities
universities --search "MIT"
universities --search "Cambridge"
universities --search "Munich"

# Export data for specific country
universities --country France --export french_universities.json

# Export all data
universities --export all_universities.json
```

### ML-Powered University Recommendations
```bash
# Find universities similar to a specific university
university-recommend --similar "Harvard University"
university-recommend --similar "Stanford"
university-recommend --similar "Oxford"

# Get recommendations based on your preferences
# Top-ranked universities
university-recommend --max-rank 50 --limit 10

# Large public universities
university-recommend --type Public --min-students 30000

# Small private universities with good rankings
university-recommend --type Private --max-students 15000 --max-rank 100

# Combine multiple filters
university-recommend --type Public --max-rank 100 --min-students 20000 --limit 15

# Train the model (already done, but you can retrain)
python -m ai_native_playground.universities.ml_model
```

### LLM-Powered University Chat
```bash
# Set your OpenAI API key (optional but recommended)
export OPENAI_API_KEY='your-api-key-here'

# Start interactive chat
university-chat

# Ask a single question
university-chat --query "Tell me about MIT"
university-chat --query "What are the top universities in the world?"
university-chat --query "Compare Oxford and Cambridge"

# Show dataset stats
university-chat --stats
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