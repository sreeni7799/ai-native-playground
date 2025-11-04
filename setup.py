#!/usr/bin/env python3
"""Setup script for AI Native Playground."""

from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="ai-native-playground",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A collection of AI-powered applications including weather API, news analyzer, and todo app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-native-playground",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[req for req in requirements if not any(dev in req for dev in ['pytest', 'black', 'flake8', 'mypy'])],
    extras_require={
        "dev": ["pytest>=7.4.3", "pytest-asyncio>=0.21.1", "black>=23.12.1", "flake8>=7.0.0", "mypy>=1.8.0"],
    },
    entry_points={
        "console_scripts": [
            "weather-api=ai_native_playground.weather_api.cli:main",
            "news-analyzer=ai_native_playground.news_analyzer.cli:main",
            "todo-app=ai_native_playground.todo_app.cli:main",
            "reddit-sentiment=ai_native_playground.reddit_sentiment.cli:main",
            "german-universities=ai_native_playground.german_universities.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)