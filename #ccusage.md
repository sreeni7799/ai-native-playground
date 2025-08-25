#ccusage report - Sreenivas Dinesh Shenoy
## Overview
This log tracks my sessions using **Claude Code CLI** for AI-native coding.  
Each entry includes session date, main prompts, and project outcomes.  

---

#### Session 1 #### - 25 August 2025

Project - CLI Todo App in Python
Prompt Used - Build a simple command-line todo app in Python with add, list, and delete features.
               Include argparse for CLI commands and save data in a local JSON file.

AI Contribution
- Generated full script with Argparse.
- Added Json persistence.
- Suggested improvements - error handling and clear UI.

Outcome - working todo.py with add/list/delete commands

---

#### Session 2 #### - 25 August 2025

Project - Understanding Todo App Usage
Prompt Used - how to run this app

AI Contribution
- Analyzed existing todo.py file
- Provided command usage instructions
- Listed all available commands (add, list, delete)

Outcome - Clear usage instructions for the Python todo app

---

#### Session 3 #### - 25 August 2025

Project - FastAPI Weather Application
Prompt Used - Develop a FastAPI project that fetches the weather data from OpenweatherMap API. Create endpoints: /current?city= Kanhangad,forecast?city=Kanhangad. Add tests with pytests

AI Contribution
- Created complete FastAPI application with async weather data fetching
- Implemented /current and /forecast endpoints with proper error handling
- Added Pydantic models for response validation
- Created comprehensive pytest test suite with mocking
- Set up project structure with requirements.txt, .env.example, and README
- Used TodoWrite tool to track all development tasks
- Updated to OneCall 3.0 API with geocoding integration
- Enhanced response models with additional weather data (UV index, feels like temperature)
- Modified tests to work with new API structure

Outcome - Full-featured weather API with OpenWeatherMap OneCall 3.0 integration, enhanced data fields, complete test coverage, and documentation

---

#### Session 4 #### - 25 August 2025

Project - News Analysis Agent System
Prompt Used - Create two Python agents: A news fetcher (scrapes headlines from a site), A summarizer (summarizes fetched headlines). Orchestrate them in one script.

AI Contribution
- Created NewsAgent class with web scraping capabilities for multiple news sources
- Built SummarizerAgent class with keyword extraction and summary generation
- Developed orchestrator script with CLI interface and multiple execution modes
- Added comprehensive demo script showing individual and coordinated usage
- Implemented error handling, progress indicators, and file output options
- Used TodoWrite tool to systematically track all development phases

Outcome - Complete multi-agent news analysis system with web scraping, text summarization, CLI orchestration, and demo examples