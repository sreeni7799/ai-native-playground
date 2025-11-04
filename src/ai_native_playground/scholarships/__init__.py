"""
Scholarships module for AI Native Playground.

Comprehensive scholarship database with ML-powered recommendations and LLM chat.
"""

from .ml_model import ScholarshipRecommendationModel
from .llm_chat import ScholarshipChatbot

__all__ = ["ScholarshipRecommendationModel", "ScholarshipChatbot"]
