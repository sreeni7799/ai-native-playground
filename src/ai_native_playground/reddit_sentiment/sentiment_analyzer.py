import re
from typing import List, Dict, Tuple
from collections import Counter
from dataclasses import dataclass


@dataclass
class SentimentScore:
    """Represents sentiment analysis results."""
    positive: float
    negative: float
    neutral: float
    compound: float
    mood: str
    confidence: float


class SentimentAnalyzer:
    """Analyzes sentiment and mood of text using lexicon-based approach."""
    
    def __init__(self):
        # Positive sentiment words with scores
        self.positive_words = {
            'amazing': 3, 'awesome': 3, 'excellent': 3, 'fantastic': 3, 'wonderful': 3,
            'great': 2, 'good': 2, 'nice': 2, 'cool': 2, 'helpful': 2, 'useful': 2,
            'interesting': 2, 'impressive': 2, 'brilliant': 3, 'outstanding': 3,
            'love': 3, 'like': 1, 'enjoy': 2, 'happy': 2, 'excited': 2, 'thrilled': 3,
            'pleased': 2, 'satisfied': 2, 'delighted': 3, 'grateful': 2, 'thankful': 2,
            'positive': 2, 'optimistic': 2, 'hopeful': 2, 'confident': 2, 'proud': 2,
            'success': 2, 'win': 2, 'victory': 3, 'achievement': 2, 'accomplish': 2,
            'perfect': 3, 'best': 3, 'better': 1, 'improve': 1, 'upgrade': 1,
            'recommend': 2, 'endorse': 2, 'support': 1, 'agree': 1, 'yes': 1,
            'exactly': 1, 'absolutely': 2, 'definitely': 2, 'certainly': 2
        }
        
        # Negative sentiment words with scores
        self.negative_words = {
            'terrible': -3, 'awful': -3, 'horrible': -3, 'disgusting': -3, 'pathetic': -3,
            'bad': -2, 'poor': -2, 'worse': -2, 'worst': -3, 'sucks': -3, 'stupid': -2,
            'hate': -3, 'dislike': -2, 'annoying': -2, 'irritating': -2, 'frustrating': -2,
            'disappointed': -2, 'upset': -2, 'angry': -3, 'furious': -3, 'outraged': -3,
            'sad': -2, 'depressed': -3, 'miserable': -3, 'unhappy': -2, 'worried': -2,
            'concerned': -1, 'anxious': -2, 'scared': -2, 'afraid': -2, 'fearful': -2,
            'negative': -2, 'pessimistic': -2, 'hopeless': -3, 'doubtful': -1, 'skeptical': -1,
            'failure': -3, 'lose': -2, 'lost': -2, 'defeat': -2, 'wrong': -1,
            'problem': -1, 'issue': -1, 'trouble': -2, 'difficulty': -1, 'challenge': -1,
            'disagree': -1, 'oppose': -2, 'against': -1, 'no': -1, 'never': -1,
            'impossible': -2, 'can\'t': -1, 'won\'t': -1, 'shouldn\'t': -1, 'wouldn\'t': -1
        }
        
        # Intensifiers
        self.intensifiers = {
            'very': 1.5, 'really': 1.5, 'extremely': 2.0, 'incredibly': 2.0, 'absolutely': 1.8,
            'completely': 1.8, 'totally': 1.8, 'quite': 1.3, 'pretty': 1.2, 'rather': 1.2,
            'so': 1.4, 'too': 1.4, 'super': 1.6, 'ultra': 1.8, 'highly': 1.5
        }
        
        # Negation words
        self.negations = {
            'not', 'no', 'never', 'none', 'nothing', 'nowhere', 'nobody', 'neither',
            'nor', 'without', 'lack', 'lacking', 'absent', 'missing', 'can\'t', 'cannot',
            'won\'t', 'wouldn\'t', 'shouldn\'t', 'couldn\'t', 'mustn\'t', 'don\'t', 'doesn\'t',
            'didn\'t', 'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t', 'haven\'t', 'hasn\'t', 'hadn\'t'
        }
    
    def analyze_comment(self, text: str) -> SentimentScore:
        """Analyze sentiment of a single comment."""
        if not text:
            return SentimentScore(0.0, 0.0, 1.0, 0.0, "neutral", 0.0)
        
        # Clean and tokenize text
        tokens = self._tokenize(text.lower())
        
        # Calculate sentiment scores
        pos_score, neg_score = self._calculate_scores(tokens)
        
        # Normalize scores
        total_words = len([t for t in tokens if t.isalpha()])
        if total_words == 0:
            return SentimentScore(0.0, 0.0, 1.0, 0.0, "neutral", 0.0)
        
        pos_normalized = max(0, pos_score / total_words)
        neg_normalized = max(0, abs(neg_score) / total_words)
        
        # Calculate compound score
        compound = (pos_score + neg_score) / total_words if total_words > 0 else 0
        
        # Determine mood and confidence
        mood, confidence = self._determine_mood(pos_normalized, neg_normalized, compound)
        
        # Calculate final normalized scores
        total_sentiment = pos_normalized + neg_normalized
        if total_sentiment > 0:
            pos_final = pos_normalized / total_sentiment
            neg_final = neg_normalized / total_sentiment
            neutral_final = 1 - pos_final - neg_final
        else:
            pos_final = 0.0
            neg_final = 0.0
            neutral_final = 1.0
        
        return SentimentScore(
            positive=pos_final,
            negative=neg_final,
            neutral=neutral_final,
            compound=compound,
            mood=mood,
            confidence=confidence
        )
    
    def analyze_comments_batch(self, comments: List[Dict]) -> Dict:
        """Analyze sentiment for a batch of comments."""
        if not comments:
            return {
                'overall_mood': 'neutral',
                'confidence': 0.0,
                'sentiment_distribution': {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0},
                'mood_breakdown': {},
                'total_comments': 0,
                'top_positive': [],
                'top_negative': []
            }
        
        sentiment_scores = []
        comment_sentiments = []
        
        for comment in comments:
            text = comment.get('body', '')
            sentiment = self.analyze_comment(text)
            sentiment_scores.append(sentiment)
            comment_sentiments.append({
                'text': text[:200],  # Truncate for display
                'sentiment': sentiment,
                'score': comment.get('score', 0)
            })
        
        # Calculate overall statistics
        total_pos = sum(s.positive for s in sentiment_scores)
        total_neg = sum(s.negative for s in sentiment_scores)
        total_neu = sum(s.neutral for s in sentiment_scores)
        total_compound = sum(s.compound for s in sentiment_scores)
        
        # Normalize
        total_comments = len(sentiment_scores)
        avg_pos = total_pos / total_comments
        avg_neg = total_neg / total_comments
        avg_neu = total_neu / total_comments
        avg_compound = total_compound / total_comments
        
        # Determine overall mood
        overall_mood, overall_confidence = self._determine_mood(avg_pos, avg_neg, avg_compound)
        
        # Get mood breakdown
        mood_counts = Counter(s.mood for s in sentiment_scores)
        mood_breakdown = {mood: count/total_comments for mood, count in mood_counts.items()}
        
        # Get top positive and negative comments
        sorted_comments = sorted(comment_sentiments, key=lambda x: x['sentiment'].compound)
        top_negative = sorted_comments[:3]  # Most negative
        top_positive = sorted_comments[-3:][::-1]  # Most positive
        
        return {
            'overall_mood': overall_mood,
            'confidence': overall_confidence,
            'sentiment_distribution': {
                'positive': avg_pos,
                'negative': avg_neg,
                'neutral': avg_neu
            },
            'compound_score': avg_compound,
            'mood_breakdown': mood_breakdown,
            'total_comments': total_comments,
            'top_positive': [{'text': c['text'], 'score': round(c['sentiment'].compound, 3)} 
                           for c in top_positive],
            'top_negative': [{'text': c['text'], 'score': round(c['sentiment'].compound, 3)} 
                           for c in top_negative]
        }
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        # Remove URLs, mentions, and special characters
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'[^a-zA-Z\s\']+', ' ', text)
        
        return text.split()
    
    def _calculate_scores(self, tokens: List[str]) -> Tuple[float, float]:
        """Calculate positive and negative sentiment scores."""
        pos_score = 0.0
        neg_score = 0.0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Check for intensifiers
            intensifier = 1.0
            if i > 0 and tokens[i-1] in self.intensifiers:
                intensifier = self.intensifiers[tokens[i-1]]
            
            # Check for negations (within 2 words)
            negated = False
            for j in range(max(0, i-2), i):
                if tokens[j] in self.negations:
                    negated = True
                    break
            
            # Calculate sentiment
            if token in self.positive_words:
                score = self.positive_words[token] * intensifier
                if negated:
                    neg_score -= score
                else:
                    pos_score += score
                    
            elif token in self.negative_words:
                score = self.negative_words[token] * intensifier
                if negated:
                    pos_score += abs(score)
                else:
                    neg_score += score
            
            i += 1
        
        return pos_score, neg_score
    
    def _determine_mood(self, pos: float, neg: float, compound: float) -> Tuple[str, float]:
        """Determine overall mood and confidence."""
        # Calculate confidence based on the difference between positive and negative
        diff = abs(pos - neg)
        confidence = min(1.0, diff * 2)  # Scale confidence
        
        if compound >= 0.05:
            if compound >= 0.5:
                return "very positive", confidence
            elif compound >= 0.2:
                return "positive", confidence
            else:
                return "slightly positive", confidence
        elif compound <= -0.05:
            if compound <= -0.5:
                return "very negative", confidence
            elif compound <= -0.2:
                return "negative", confidence
            else:
                return "slightly negative", confidence
        else:
            return "neutral", confidence