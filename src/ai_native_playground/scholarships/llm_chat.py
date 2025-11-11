"""
Scholarship Chatbot with LLM Integration

RAG (Retrieval Augmented Generation) system for scholarship queries.
Uses TF-IDF for retrieval and OpenAI GPT for natural language responses.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class ScholarshipChatbot:
    """
    LLM-powered chatbot for scholarship information.

    Features:
    - TF-IDF-based retrieval for relevant scholarships
    - OpenAI GPT integration for natural language responses
    - Fallback mode when OpenAI API is unavailable
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chatbot."""
        self.data_path = Path(__file__).parent / "data" / "scholarships_4000_dataset.json"

        # Load scholarship data
        self.scholarships = self._load_scholarships()

        # Defer TF-IDF initialization until first query (truly lazy loading)
        self.vectorizer = None
        self.tfidf_matrix = None
        self.scholarship_texts = None
        self._retrieval_initialized = False

        # Initialize OpenAI client
        self.llm_available = False
        self.client = None

        # Get API key
        api_key = api_key or os.getenv('OPENAI_API_KEY')

        if api_key and api_key != 'your_openai_api_key_here':
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                self.llm_available = True
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")

    def _load_scholarships(self) -> List[Dict[str, Any]]:
        """Load scholarship dataset."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Scholarship dataset not found: {self.data_path}")

        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data['scholarships']

    def _create_searchable_texts(self) -> List[str]:
        """Create searchable text representation for each scholarship."""
        texts = []

        for s in self.scholarships:
            text_parts = [
                s.get('name', ''),
                s.get('provider', ''),
                s.get('country', ''),
                s.get('type', ''),
                s.get('field', ''),
                s.get('level', ''),
                s.get('description', ''),
                f"amount {s.get('amount', 0)}",
                "renewable" if s.get('renewable') else "non-renewable"
            ]
            texts.append(' '.join(str(p) for p in text_parts))

        return texts

    def _initialize_retrieval(self):
        """Initialize TF-IDF vectorizer for document retrieval (lazy loading)."""
        try:
            # Lazy import to avoid startup errors
            from sklearn.feature_extraction.text import TfidfVectorizer

            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words='english'
            )

            # Create searchable text for each scholarship
            self.scholarship_texts = self._create_searchable_texts()

            # Fit vectorizer
            self.tfidf_matrix = self.vectorizer.fit_transform(self.scholarship_texts)
            self._retrieval_initialized = True
        except ImportError as e:
            print(f"Warning: sklearn not available - {e}. Using fallback mode.")
            self._retrieval_initialized = False

    def retrieve_relevant_scholarships(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.001
    ) -> List[Dict[str, Any]]:
        """
        Retrieve scholarships relevant to the query using TF-IDF.

        Args:
            query: User query
            top_k: Number of scholarships to retrieve
            min_similarity: Minimum similarity threshold

        Returns:
            List of relevant scholarships with similarity scores
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

        # Expand query with common synonyms
        query_expanded = self._expand_query(query)

        # Vectorize query
        query_vec = self.vectorizer.transform([query_expanded])

        # Calculate similarities
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k * 2]

        # Filter by minimum similarity
        results = []
        for idx in top_indices:
            if similarities[idx] >= min_similarity:
                scholarship = self.scholarships[idx].copy()
                scholarship['similarity_score'] = float(similarities[idx])
                results.append(scholarship)

        # If no results with TF-IDF, use high-value scholarships
        if len(results) == 0:
            # Check for "best" or "top" queries
            if any(word in query.lower() for word in ['best', 'top', 'highest', 'good', 'great']):
                sorted_scholarships = sorted(
                    self.scholarships,
                    key=lambda x: x.get('amount', 0),
                    reverse=True
                )
                results = sorted_scholarships[:top_k]

        return results[:top_k]

    def _simple_keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search when sklearn is not available."""
        query_lower = query.lower()
        keywords = query_lower.split()

        # Score each scholarship by keyword matches
        scored_scholarships = []
        for scholarship in self.scholarships:
            score = 0
            scholarship_text = f"{scholarship.get('name', '')} {scholarship.get('provider', '')} {scholarship.get('country', '')} {scholarship.get('type', '')} {scholarship.get('field', '')} {scholarship.get('level', '')}".lower()

            for keyword in keywords:
                if keyword in scholarship_text:
                    score += 1

            # Check for special keywords
            if 'renewable' in query_lower and scholarship.get('renewable'):
                score += 2
            if 'international' in query_lower and scholarship.get('level') == 'International':
                score += 2

            # Check amount if specified in query
            if any(amount_word in query_lower for amount_word in ['over', 'above', 'high', 'large']):
                if scholarship.get('amount', 0) > 30000:
                    score += 1

            if score > 0:
                scholarship_copy = scholarship.copy()
                scholarship_copy['similarity_score'] = float(score) / len(keywords)
                scored_scholarships.append(scholarship_copy)

        # Sort by score and return top-k
        scored_scholarships.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_scholarships[:top_k] if scored_scholarships else self.scholarships[:top_k]

    def _expand_query(self, query: str) -> str:
        """Expand query with synonyms and related terms."""
        query_lower = query.lower()

        # Add field expansions
        if 'engineering' in query_lower or 'engineer' in query_lower:
            query += ' technology stem technical'
        if 'computer science' in query_lower or 'cs' in query_lower:
            query += ' technology programming software'
        if 'medicine' in query_lower or 'medical' in query_lower:
            query += ' health healthcare doctor'
        if 'business' in query_lower:
            query += ' management mba entrepreneurship'

        # Add level expansions
        if 'undergraduate' in query_lower:
            query += ' bachelor bachelors'
        if 'graduate' in query_lower or 'masters' in query_lower:
            query += ' postgraduate phd doctoral'

        # Add type expansions
        if 'merit' in query_lower:
            query += ' academic excellence achievement'
        if 'need' in query_lower:
            query += ' financial aid assistance'

        return query

    def chat(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and return a response.

        Args:
            query: User query

        Returns:
            Dictionary with response and metadata
        """
        # Retrieve relevant scholarships
        relevant_scholarships = self.retrieve_relevant_scholarships(query, top_k=5)

        if self.llm_available and relevant_scholarships:
            # Use LLM for response
            response = self._generate_llm_response(query, relevant_scholarships)
            using_llm = True
        else:
            # Fallback response
            response = self._generate_fallback_response(query, relevant_scholarships)
            using_llm = False

        return {
            'response': response,
            'scholarships_found': len(relevant_scholarships),
            'using_llm': using_llm
        }

    def _generate_llm_response(
        self,
        query: str,
        scholarships: List[Dict[str, Any]]
    ) -> str:
        """Generate response using OpenAI GPT."""
        # Format scholarship data for context
        context = self._format_scholarships_for_context(scholarships)

        # Create prompt
        system_prompt = """You are a helpful scholarship advisor assistant.
You have access to a database of 4,000+ scholarships worldwide.
Provide accurate, helpful information about scholarships based on the data provided.
Format amounts in currency (e.g., $50,000).
Be concise but informative."""

        user_prompt = f"""Based on this scholarship data:

{context}

User question: {query}

Please provide a helpful response about these scholarships. Include specific details like amounts, providers, and eligibility when relevant."""

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

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"LLM error: {e}")
            return self._generate_fallback_response(query, scholarships)

    def _format_scholarships_for_context(
        self,
        scholarships: List[Dict[str, Any]]
    ) -> str:
        """Format scholarships for LLM context."""
        formatted = []

        for i, s in enumerate(scholarships, 1):
            renewable_text = "renewable annually" if s.get('renewable') else "one-time"
            deadline = s.get('deadline', 'Rolling')

            text = f"""{i}. {s['name']}
   Provider: {s['provider']}
   Amount: ${s['amount']:,} ({renewable_text})
   Country: {s['country']}
   Type: {s['type']}
   Field: {s['field']}
   Level: {s['level']}
   Deadline: {deadline}
   Description: {s.get('description', 'N/A')}"""

            formatted.append(text)

        return '\n\n'.join(formatted)

    def _generate_fallback_response(
        self,
        query: str,
        scholarships: List[Dict[str, Any]]
    ) -> str:
        """Generate simple response without LLM."""
        if not scholarships:
            return ("I couldn't find scholarships matching your query. "
                   "Try being more specific about country, field of study, or scholarship type.")

        response_parts = [f"Found {len(scholarships)} relevant scholarship(s):\n"]

        for i, s in enumerate(scholarships, 1):
            renewable_text = " (renewable)" if s.get('renewable') else ""
            response_parts.append(
                f"{i}. {s['name']}\n"
                f"   Amount: ${s['amount']:,}{renewable_text}\n"
                f"   Provider: {s['provider']}\n"
                f"   Country: {s['country']}\n"
                f"   Field: {s['field']} | Level: {s['level']}\n"
                f"   Type: {s['type']}"
            )

        return '\n\n'.join(response_parts)

    def get_statistics_response(self) -> str:
        """Generate statistics about the scholarship database."""
        # Count by country
        countries = {}
        for s in self.scholarships:
            country = s.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1

        # Count by type
        types = {}
        for s in self.scholarships:
            typ = s.get('type', 'Unknown')
            types[typ] = types.get(typ, 0) + 1

        # Count by field
        fields = {}
        for s in self.scholarships:
            field = s.get('field', 'Unknown')
            fields[field] = fields.get(field, 0) + 1

        # Count by level
        levels = {}
        for s in self.scholarships:
            level = s.get('level', 'Unknown')
            levels[level] = levels.get(level, 0) + 1

        # Calculate amount statistics
        amounts = [s.get('amount', 0) for s in self.scholarships]
        avg_amount = sum(amounts) / len(amounts) if amounts else 0
        max_amount = max(amounts) if amounts else 0

        # Count renewable
        renewable_count = sum(1 for s in self.scholarships if s.get('renewable'))

        response = f"""📊 Scholarship Database Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Scholarships: {len(self.scholarships):,}

💰 Amount Statistics:
  • Average Amount: ${avg_amount:,.0f}
  • Maximum Amount: ${max_amount:,}
  • Renewable: {renewable_count} ({renewable_count/len(self.scholarships)*100:.1f}%)

🌍 Top Countries:
{self._format_top_items(countries, 10)}

📚 By Field of Study:
{self._format_top_items(fields, 8)}

🎓 By Level:
{self._format_top_items(levels)}

📋 By Type:
{self._format_top_items(types)}
"""

        return response

    def _format_top_items(self, items_dict: Dict[str, int], limit: int = 5) -> str:
        """Format dictionary items for display."""
        sorted_items = sorted(items_dict.items(), key=lambda x: x[1], reverse=True)[:limit]
        return '\n'.join(f"  • {name}: {count}" for name, count in sorted_items)


if __name__ == "__main__":
    # Test the chatbot
    print("Initializing Scholarship Chatbot...")
    chatbot = ScholarshipChatbot()

    print(f"✓ Loaded {len(chatbot.scholarships)} scholarships")
    print(f"✓ LLM Available: {chatbot.llm_available}")

    # Test queries
    test_queries = [
        "Show me engineering scholarships",
        "What scholarships are available in UK?",
        "Tell me about Fulbright scholarship",
        "High-value renewable scholarships"
    ]

    print("\n" + "="*80)
    print("TESTING SCHOLARSHIP CHATBOT")
    print("="*80 + "\n")

    for query in test_queries:
        print(f"Query: {query}")
        result = chatbot.chat(query)
        print(f"Response ({result['scholarships_found']} found):")
        print(result['response'])
        print("\n" + "-"*80 + "\n")
