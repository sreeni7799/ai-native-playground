#!/usr/bin/env python3

import argparse
import time
from typing import List, Dict
from .news_agent import NewsAgent
from .summarizer_agent import SummarizerAgent

class NewsOrchestrator:
    def __init__(self):
        self.news_agent = None
        self.summarizer = SummarizerAgent()
    
    def run_news_analysis(self, news_sources: List[str], max_headlines: int = 10, save_to_file: bool = False) -> Dict:
        print("🚀 Starting news analysis pipeline...\n")
        
        all_headlines = []
        
        for source_url in news_sources:
            print(f"📰 Fetching from: {source_url}")
            self.news_agent = NewsAgent(source_url)
            headlines = self.news_agent.fetch_headlines(max_headlines)
            all_headlines.extend(headlines)
            time.sleep(1)
        
        print(f"\n📊 Total headlines collected: {len(all_headlines)}")
        
        if not all_headlines:
            print("❌ No headlines found. Please check your news sources.")
            return {}
        
        print("\n🔍 Analyzing and summarizing headlines...")
        summary_data = self.summarizer.summarize_headlines(all_headlines)
        
        detailed_report = self.summarizer.generate_detailed_report(all_headlines)
        print(f"\n{detailed_report}")
        
        if save_to_file:
            filename = f"news_summary_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(detailed_report)
            print(f"\n💾 Report saved to: {filename}")
        
        return {
            'headlines': all_headlines,
            'summary': summary_data,
            'report': detailed_report
        }

def main():
    parser = argparse.ArgumentParser(description="News Analysis Orchestrator - Fetch and Summarize Headlines")
    parser.add_argument('--sources', '-s', nargs='+', 
                       default=['https://news.ycombinator.com'],
                       help='News source URLs to scrape (default: Hacker News)')
    parser.add_argument('--max-headlines', '-m', type=int, default=15,
                       help='Maximum headlines per source (default: 15)')
    parser.add_argument('--save', action='store_true',
                       help='Save report to file')
    parser.add_argument('--quick', action='store_true',
                       help='Quick run with fewer headlines')
    
    args = parser.parse_args()
    
    if args.quick:
        args.max_headlines = 5
        print("⚡ Quick mode: Fetching 5 headlines per source\n")
    
    orchestrator = NewsOrchestrator()
    
    try:
        result = orchestrator.run_news_analysis(
            news_sources=args.sources,
            max_headlines=args.max_headlines,
            save_to_file=args.save
        )
        
        if result:
            print("\n✅ News analysis completed successfully!")
        else:
            print("\n❌ News analysis failed - no data retrieved")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()