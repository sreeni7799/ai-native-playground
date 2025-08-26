.PHONY: help install install-dev test lint format type-check clean build
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install the package in development mode with dev dependencies
	pip install -e .[dev]

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src/ai_native_playground --cov-report=html --cov-report=term

lint: ## Run linting checks
	flake8 src/

format: ## Format code with black
	black src/

format-check: ## Check code formatting
	black --check src/

type-check: ## Run type checking
	mypy src/ai_native_playground

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

build: ## Build the package
	python -m build

check: lint format-check type-check test ## Run all checks

# Application shortcuts
weather: ## Start the weather API server
	weather-api

news: ## Run news analyzer
	news-analyzer

todo: ## Run todo app help
	todo-app

reddit: ## Start Reddit sentiment analyzer
	reddit-sentiment