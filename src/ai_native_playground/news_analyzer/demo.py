#!/usr/bin/env python3

from news_agent import NewsAgent
from summarizer_agent import SummarizerAgent

def demo_individual_agents():
    print("=== DEMO: Individual Agent Testing ===\n")
    
    print("1. Testing NewsAgent with Hacker News:")
    news_agent = NewsAgent("https://news.ycombinator.com")
    headlines = news_agent.fetch_headlines(5)
    
    for i, headline in enumerate(headlines, 1):
        print(f"  {i}. {headline['title']}")
        print(f"     Source: {headline['source']}")
        print(f"     URL: {headline['url'][:50]}..." if len(headline['url']) > 50 else f"     URL: {headline['url']}")
        print()
    
    print("\n2. Testing SummarizerAgent:")
    summarizer = SummarizerAgent()
    summary = summarizer.summarize_headlines(headlines)
    
    print(f"   Total Headlines: {summary['total_headlines']}")
    print(f"   Key Topics: {', '.join(summary['key_topics'][:5])}")
    print(f"   Summary: {summary['summary']}")
    
    print("\n3. Generating Detailed Report:")
    report = summarizer.generate_detailed_report(headlines)
    print(report)

def demo_orchestrator():
    print("\n\n=== DEMO: Orchestrator Usage ===\n")
    from news_orchestrator import NewsOrchestrator
    
    orchestrator = NewsOrchestrator()
    result = orchestrator.run_news_analysis(
        news_sources=["https://news.ycombinator.com"],
        max_headlines=8,
        save_to_file=False
    )
    
    if result:
        print(f"\n✅ Successfully processed {len(result['headlines'])} headlines")
        print(f"🔍 Found {len(result['summary']['key_topics'])} trending topics")

if __name__ == "__main__":
    print("🤖 News Agents Demo\n")
    print("This demo showcases the NewsAgent and SummarizerAgent working together.")
    print("=" * 60)
    
    try:
        demo_individual_agents()
        demo_orchestrator()
        
        print("\n" + "=" * 60)
        print("📚 USAGE EXAMPLES:")
        print("1. Basic run:           python news_orchestrator.py")
        print("2. Multiple sources:    python news_orchestrator.py -s https://news.ycombinator.com")  
        print("3. Save to file:        python news_orchestrator.py --save")
        print("4. Quick mode:          python news_orchestrator.py --quick")
        print("5. More headlines:      python news_orchestrator.py -m 20")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have internet connection and required dependencies installed.")