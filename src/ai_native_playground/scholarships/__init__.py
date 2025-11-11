"""
Scholarships module for AI Native Playground.

Comprehensive scholarship database with ML-powered recommendations and LLM chat.
"""

__all__ = ["ScholarshipRecommendationModel", "ScholarshipChatbot"]


def __getattr__(name):
    """Lazy import to avoid import errors during package installation."""
    if name == "ScholarshipRecommendationModel":
        from .ml_model import ScholarshipRecommendationModel
        return ScholarshipRecommendationModel
    elif name == "ScholarshipChatbot":
        from .llm_chat import ScholarshipChatbot
        return ScholarshipChatbot
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
