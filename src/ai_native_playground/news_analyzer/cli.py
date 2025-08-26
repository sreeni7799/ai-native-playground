#!/usr/bin/env python3
"""Command-line interface for the News Analyzer."""

import argparse
import time
from .news_orchestrator import NewsOrchestrator


def main():
    """Run the news analyzer CLI."""
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