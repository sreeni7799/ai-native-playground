from typing import List, Dict
import re
from collections import Counter

class SummarizerAgent:
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'can', 'may', 'might', 'must', 'this', 'that', 'these', 'those', 'i',
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my',
            'your', 'his', 'her', 'its', 'our', 'their'
        }
    
    def summarize_headlines(self, headlines: List[Dict]) -> Dict:
        if not headlines:
            return {
                'total_headlines': 0,
                'key_topics': [],
                'summary': 'No headlines to summarize.',
                'sources': []
            }
        
        titles = [headline['title'] for headline in headlines]
        sources = [headline.get('source', 'Unknown') for headline in headlines]
        
        key_topics = self._extract_key_topics(titles)
        summary = self._generate_summary(titles, key_topics)
        source_counts = Counter(sources)
        
        result = {
            'total_headlines': len(headlines),
            'key_topics': key_topics[:10],
            'summary': summary,
            'sources': dict(source_counts),
            'headlines_preview': titles[:3]
        }
        
        print(f"✓ Summarized {len(headlines)} headlines into key insights")
        return result
    
    def _extract_key_topics(self, titles: List[str]) -> List[str]:
        all_words = []
        
        for title in titles:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
            filtered_words = [word for word in words if word not in self.stop_words]
            all_words.extend(filtered_words)
        
        word_counts = Counter(all_words)
        return [word.title() for word, count in word_counts.most_common(15) if count > 1]
    
    def _generate_summary(self, titles: List[str], key_topics: List[str]) -> str:
        total = len(titles)
        
        if not titles:
            return "No headlines available for summary."
        
        tech_keywords = ['ai', 'tech', 'software', 'app', 'data', 'api', 'cloud', 'startup']
        business_keywords = ['company', 'market', 'stock', 'investment', 'business', 'ceo']
        
        tech_count = sum(1 for title in titles if any(kw in title.lower() for kw in tech_keywords))
        business_count = sum(1 for title in titles if any(kw in title.lower() for kw in business_keywords))
        
        summary_parts = [
            f"Analyzed {total} headlines from news sources."
        ]
        
        if key_topics:
            top_topics = key_topics[:5]
            summary_parts.append(f"Key topics trending: {', '.join(top_topics)}.")
        
        if tech_count > total * 0.3:
            summary_parts.append(f"Strong technology focus ({tech_count} tech-related headlines).")
        
        if business_count > total * 0.3:
            summary_parts.append(f"Significant business coverage ({business_count} business headlines).")
        
        return " ".join(summary_parts)
    
    def generate_detailed_report(self, headlines: List[Dict]) -> str:
        summary_data = self.summarize_headlines(headlines)
        
        report = []
        report.append("=== NEWS SUMMARY REPORT ===\n")
        report.append(f"Total Headlines Analyzed: {summary_data['total_headlines']}")
        report.append(f"News Sources: {', '.join(summary_data['sources'].keys())}\n")
        
        report.append("📋 EXECUTIVE SUMMARY:")
        report.append(f"{summary_data['summary']}\n")
        
        if summary_data['key_topics']:
            report.append("🔥 TOP TRENDING TOPICS:")
            for i, topic in enumerate(summary_data['key_topics'][:10], 1):
                report.append(f"  {i}. {topic}")
            report.append("")
        
        report.append("📰 SAMPLE HEADLINES:")
        for i, headline in enumerate(summary_data['headlines_preview'], 1):
            report.append(f"  {i}. {headline}")
        
        return "\n".join(report)