"""
LLM-Powered University Chat System

This module implements a Retrieval Augmented Generation (RAG) system for
answering questions about universities using an LLM with the university dataset.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

        # Initialize retrieval system
        self._initialize_retrieval()

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

    def generate_response(self, query: str, context: str) -> str:
        """
        Generate response using LLM with retrieved context.

        Args:
            query: User query
            context: Retrieved university data

        Returns:
            Generated response
        """
        if not self.llm_available:
            return self._generate_fallback_response(context)

        system_prompt = """You are a knowledgeable university advisor assistant.
You help students find and learn about universities around the world.
Use the provided university data to answer questions accurately and helpfully.
Be concise but informative. If asked to compare universities, provide balanced insights.
If the data doesn't contain information to answer the question, say so politely."""

        user_prompt = f"""Based on the following university information, please answer this question:

Question: {query}

University Data:
{context}

Please provide a helpful, accurate response based on the data above."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
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

    def chat(self, query: str) -> Dict[str, Any]:
        """
        Main chat interface.

        Args:
            query: User query about universities

        Returns:
            Dictionary with response and metadata
        """
        # Retrieve relevant universities
        universities = self.retrieve_relevant_universities(query, top_k=5)

        # Format context
        context = self.format_university_context(universities)

        # Generate response
        response = self.generate_response(query, context)

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
