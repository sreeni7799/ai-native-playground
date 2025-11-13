"""
LLM-Powered University Chat System

This module implements a Retrieval Augmented Generation (RAG) system for
answering questions about universities using an LLM with the university dataset.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class UniversityChatbot:
    """
    RAG-based chatbot for university queries.

    Features:
    - Retrieves relevant universities from the dataset
    - Uses LLM to generate natural responses
    - Context-aware conversation
    - Supports multiple query types
    """

    def __init__(self, use_openai: bool = True, api_key: Optional[str] = None):
        """
        Initialize the chatbot.

        Args:
            use_openai: Whether to use OpenAI API (requires API key)
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        self.use_openai = use_openai
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        # Load university data - try 4k dataset first, fallback to 1k
        self.data_path_4k = Path(__file__).parent / "data" / "universities_4000_dataset.json"
        self.data_path_1k = Path(__file__).parent / "data" / "universities_1000_dataset.json"

        if self.data_path_4k.exists():
            self.data_path = self.data_path_4k
        else:
            self.data_path = self.data_path_1k

        self.universities = self._load_universities()

        # Defer retrieval initialization until first query (truly lazy loading)
        self.vectorizer = None
        self.doc_vectors = None
        self._retrieval_initialized = False

        # Initialize LLM if available
        if self.use_openai and self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.llm_available = True
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.llm_available = False
        else:
            self.llm_available = False

    def _load_universities(self) -> List[Dict[str, Any]]:
        """Load and flatten the university dataset."""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        universities = []
        for country, unis in data.items():
            for uni in unis:
                uni['country'] = country.replace('_', ' ').title()
                universities.append(uni)

        return universities

    def _initialize_retrieval(self):
        """Initialize TF-IDF vectorizer for document retrieval."""
        try:
            # Lazy import to avoid startup errors
            from sklearn.feature_extraction.text import TfidfVectorizer

            # Create searchable text for each university
            documents = []
            for uni in self.universities:
                text_parts = [
                    uni['name'],
                    uni.get('city', ''),
                    uni['country'],
                    uni['type'],
                    f"ranking {uni.get('ranking', '')}",
                    f"students {uni.get('students', '')}",
                    f"founded {uni.get('founded', '')}"
                ]

                # Add notable programs if available
                if 'notable_programs' in uni:
                    text_parts.extend(uni['notable_programs'])

                documents.append(' '.join(str(p) for p in text_parts))

            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=1000,
                ngram_range=(1, 2),
                min_df=1
            )
            self.doc_vectors = self.vectorizer.fit_transform(documents)
            self._retrieval_initialized = True
        except ImportError as e:
            print(f"Warning: sklearn not available - {e}. Using fallback mode.")
            self._retrieval_initialized = False

    def retrieve_relevant_universities(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve universities relevant to the query.

        Args:
            query: User query
            top_k: Number of universities to retrieve

        Returns:
            List of relevant universities
        """
        # Ensure retrieval system is initialized (truly lazy loading)
        if not self._retrieval_initialized:
            self._initialize_retrieval()

        # If sklearn not available, use simple keyword matching
        if not self._retrieval_initialized:
            return self._simple_keyword_search(query, top_k)

        # Lazy imports to avoid startup errors
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        # Vectorize query
        query_vector = self.vectorizer.transform([query])

        # Calculate similarity
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Return universities with similarity scores
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.001:  # Lower threshold for better recall
                uni = self.universities[idx].copy()
                uni['relevance_score'] = float(similarities[idx])
                results.append(uni)

        # Fallback: if no results and query mentions "top" or "best", return top-ranked
        if not results and any(word in query.lower() for word in ['top', 'best', 'leading', 'prestigious']):
            sorted_unis = sorted(self.universities, key=lambda x: x.get('ranking', 9999))
            results = sorted_unis[:top_k]
            for uni in results:
                uni['relevance_score'] = 0.9

        return results

    def _simple_keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search when sklearn is not available."""
        import re

        query_lower = query.lower()
        keywords = query_lower.split()

        # Remove common words
        stop_words = {'the', 'in', 'at', 'of', 'for', 'and', 'or', 'a', 'an', 'country', 'best', 'top', 'show', 'me', 'university', 'universities'}
        keywords = [k for k in keywords if k not in stop_words]

        # Score each university by keyword matches
        scored_unis = []
        for uni in self.universities:
            score = 0

            # Create searchable fields with word boundaries
            name_lower = uni['name'].lower()
            city_lower = uni.get('city', '').lower()
            country_lower = uni['country'].lower()
            type_lower = uni['type'].lower()

            for keyword in keywords:
                # Use word boundary matching to avoid "india" matching "indianapolis"
                pattern = r'\b' + re.escape(keyword) + r'\b'

                if re.search(pattern, name_lower):
                    score += 3  # Name match is most important
                if re.search(pattern, country_lower):
                    score += 5  # Country match is very important
                if re.search(pattern, city_lower):
                    score += 2
                if re.search(pattern, type_lower):
                    score += 1

            if score > 0:
                uni_copy = uni.copy()
                uni_copy['relevance_score'] = float(score) / max(len(keywords), 1)
                scored_unis.append(uni_copy)

        # Sort by score and return top-k
        scored_unis.sort(key=lambda x: x['relevance_score'], reverse=True)

        # If no results, return top-ranked universities
        if not scored_unis:
            sorted_unis = sorted(self.universities, key=lambda x: x.get('ranking', 9999))
            return sorted_unis[:top_k]

        return scored_unis[:top_k]

    def format_university_context(self, universities: List[Dict[str, Any]]) -> str:
        """Format university data as context for the LLM."""
        if not universities:
            return "No universities found matching the query."

        context_parts = []
        for i, uni in enumerate(universities, 1):
            parts = [
                f"\n{i}. {uni['name']}",
                f"   Location: {uni.get('city', 'N/A')}, {uni['country']}",
                f"   Type: {uni['type']}",
                f"   Founded: {uni.get('founded', 'N/A')}",
                f"   Students: {uni.get('students', 'N/A'):,}" if uni.get('students') else "",
                f"   World Ranking: #{uni.get('ranking', 'N/A')}"
            ]

            if 'notable_programs' in uni:
                parts.append(f"   Notable Programs: {', '.join(uni['notable_programs'])}")

            context_parts.append('\n'.join(p for p in parts if p))

        return '\n'.join(context_parts)

    def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate response using LLM with retrieved context.

        Args:
            query: User query
            context: Retrieved university data
            conversation_history: Previous conversation messages
            user_profile: User's academic profile for personalization

        Returns:
            Generated response
        """
        if not self.llm_available:
            return self._generate_fallback_response(context)

        # Build system prompt with personality
        system_prompt = """You are an intelligent, friendly university advisor assistant - like a knowledgeable friend helping students navigate their education journey.

Your personality:
- Conversational and warm, not robotic
- Vary your responses - don't give identical answers to similar questions
- Remember context from the conversation
- Provide personalized recommendations based on the user's profile
- Be encouraging and supportive
- Use natural language, occasional emojis, and varied sentence structures

When answering:
- Vary your opening phrases (don't always start the same way)
- Provide specific details from the university data
- If user shares their profile (GPA, test scores, field of study), use it to give tailored advice
- Compare and contrast when relevant
- Highlight key differentiators between universities
- Be honest about competitiveness and requirements"""

        # Build user prompt with conversation history and profile
        user_prompt_parts = []

        # Add user profile if available
        if user_profile:
            profile_info = []
            if user_profile.get('degree'):
                profile_info.append(f"Degree Level: {user_profile['degree']}")
            if user_profile.get('field'):
                profile_info.append(f"Field of Study: {user_profile['field']}")
            if user_profile.get('gpa'):
                profile_info.append(f"GPA: {user_profile['gpa']}")
            if user_profile.get('test_scores'):
                scores = ', '.join([f"{k}: {v}" for k, v in user_profile['test_scores'].items()])
                profile_info.append(f"Test Scores: {scores}")
            if user_profile.get('budget'):
                profile_info.append(f"Budget: ${user_profile['budget']:,}")
            if user_profile.get('countries'):
                profile_info.append(f"Preferred Countries: {', '.join(user_profile['countries'])}")

            if profile_info:
                user_prompt_parts.append(f"Student Profile:\n" + '\n'.join(f"- {info}" for info in profile_info))

        # Add conversation history for context
        if conversation_history and len(conversation_history) > 0:
            history_text = "Previous conversation:\n"
            for msg in conversation_history[-6:]:  # Last 3 exchanges
                role = "Student" if msg['role'] == 'user' else "You"
                history_text += f"{role}: {msg['content']}\n"
            user_prompt_parts.append(history_text)

        # Add current query and university data
        user_prompt_parts.append(f"""Current question: {query}

Relevant University Data:
{context}

Please provide a natural, conversational, and personalized response. If you mentioned something about these universities in the previous conversation, build on that rather than repeating. If the student shared their profile, use it to give tailored recommendations.""")

        user_prompt = '\n\n'.join(user_prompt_parts)

        try:
            # Build messages list for OpenAI
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-6:]:
                    messages.append({"role": msg['role'], "content": msg['content']})

            # Add current query
            messages.append({"role": "user", "content": user_prompt})

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,  # Higher for more varied responses
                max_tokens=600,
                presence_penalty=0.6,  # Reduce repetition
                frequency_penalty=0.3
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._generate_fallback_response(context)

    def _generate_fallback_response(self, context: str) -> str:
        """Generate a simple response without LLM."""
        return f"""Based on the university database, here are the relevant results:

{context}

Note: For more detailed analysis and natural language responses, please set your OPENAI_API_KEY environment variable."""

    def chat(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main chat interface with conversation memory and personalization.

        Args:
            query: User query about universities
            conversation_history: Previous conversation messages
            user_profile: User's academic profile for personalization

        Returns:
            Dictionary with response and metadata
        """
        # Retrieve relevant universities
        universities = self.retrieve_relevant_universities(query, top_k=5)

        # Format context
        context = self.format_university_context(universities)

        # Generate response with history and profile
        response = self.generate_response(
            query,
            context,
            conversation_history=conversation_history,
            user_profile=user_profile
        )

        return {
            'query': query,
            'response': response,
            'universities_found': len(universities),
            'universities': universities,
            'using_llm': self.llm_available
        }

    def get_statistics_response(self) -> str:
        """Get statistics about the dataset."""
        total = len(self.universities)
        by_country = {}
        for uni in self.universities:
            country = uni['country']
            by_country[country] = by_country.get(country, 0) + 1

        stats = [
            f"I have information about {total} universities worldwide.",
            "\nUniversities by country:"
        ]
        for country, count in sorted(by_country.items()):
            stats.append(f"  • {country}: {count} universities")

        stats.append("\nYou can ask me questions like:")
        stats.append("  • 'Tell me about Harvard University'")
        stats.append("  • 'What are the top engineering schools?'")
        stats.append("  • 'Compare Oxford and Cambridge'")
        stats.append("  • 'Which universities have the most students?'")
        stats.append("  • 'Show me universities in Germany'")

        return '\n'.join(stats)


def demo():
    """Demo the chatbot with sample queries."""
    print("="*80)
    print("UNIVERSITY CHATBOT DEMO")
    print("="*80)

    chatbot = UniversityChatbot()

    if chatbot.llm_available:
        print("✓ Using OpenAI GPT-3.5 for responses")
    else:
        print("⚠ OpenAI API not available. Using fallback mode.")
        print("  Set OPENAI_API_KEY environment variable for full LLM responses.")

    print("\n" + chatbot.get_statistics_response())

    # Sample queries
    sample_queries = [
        "Tell me about MIT",
        "What are the top universities in Canada?",
        "Which universities are best for engineering?"
    ]

    print("\n" + "="*80)
    print("SAMPLE QUERIES")
    print("="*80)

    for query in sample_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 80)

        result = chatbot.chat(query)
        print(result['response'])
        print(f"\n📊 Found {result['universities_found']} relevant universities")


if __name__ == "__main__":
    demo()
