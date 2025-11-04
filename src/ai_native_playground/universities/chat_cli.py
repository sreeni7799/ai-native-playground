"""
Interactive CLI for University Chatbot

Chat with an LLM to get information about universities worldwide.
"""

import argparse
import sys
import os
from pathlib import Path
from .llm_chat import UniversityChatbot


def print_header():
    """Print welcome header."""
    print("\n" + "="*80)
    print("🎓 UNIVERSITY CHATBOT - Powered by LLM + 1000 Universities Dataset")
    print("="*80)


def print_help():
    """Print help information."""
    help_text = """
Available Commands:
  - Type your question to get information about universities
  - 'stats' or 'info' - Show dataset statistics
  - 'examples' - Show example queries
  - 'help' - Show this help message
  - 'quit' or 'exit' - Exit the chatbot

Example Questions:
  • "Tell me about Stanford University"
  • "What are the best universities in Canada?"
  • "Compare Harvard and MIT"
  • "Which universities have over 50,000 students?"
  • "Show me top-ranked universities in Europe"
  • "What universities are good for engineering?"
  • "Tell me about universities in Berlin"
"""
    print(help_text)


def print_examples():
    """Print example queries."""
    examples = """
Example Queries to Try:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Specific University Information:
   • "Tell me about Harvard University"
   • "What can you tell me about the University of Toronto?"
   • "Give me details about Technical University of Munich"

2. Country/Location Queries:
   • "What are the top universities in Germany?"
   • "Show me universities in Australia"
   • "Which UK universities have the best rankings?"

3. Ranking and Quality:
   • "What are the top 5 universities in the world?"
   • "Which universities rank in the top 50?"
   • "Compare the rankings of Oxford and Cambridge"

4. Size and Type:
   • "Which universities have over 40,000 students?"
   • "What are the largest universities?"
   • "Show me small private universities"

5. Comparison:
   • "Compare Stanford and MIT"
   • "What's the difference between public and private universities?"
   • "Compare universities in the US vs UK"

6. Programs and Specialties:
   • "Which universities are best for engineering?"
   • "Show me universities strong in computer science"
   • "What schools have good medicine programs?"
"""
    print(examples)


def interactive_mode(chatbot: UniversityChatbot):
    """Run interactive chat mode."""
    print_header()

    if chatbot.llm_available:
        print("✓ Connected to OpenAI GPT-3.5")
        print("✓ Loaded 1000 universities from 6 countries")
    else:
        print("⚠ Running in fallback mode (OpenAI API not configured)")
        print("  For full LLM responses, set: export OPENAI_API_KEY='your-key-here'")
        print("✓ Loaded 1000 universities from 6 countries")

    print("\nType 'help' for commands, 'quit' to exit")
    print("="*80)

    while True:
        try:
            # Get user input
            print("\n💬 You: ", end='')
            query = input().strip()

            if not query:
                continue

            # Handle commands
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using University Chatbot!")
                break

            elif query.lower() in ['help', 'h', '?']:
                print_help()
                continue

            elif query.lower() in ['stats', 'info', 'statistics']:
                print("\n" + chatbot.get_statistics_response())
                continue

            elif query.lower() in ['examples', 'example']:
                print_examples()
                continue

            # Process query
            print("\n🤖 Assistant: ", end='', flush=True)
            result = chatbot.chat(query)

            print(result['response'])

            # Show metadata
            if result['universities_found'] > 0:
                print(f"\n📊 Retrieved {result['universities_found']} universities for this response")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


def single_query_mode(chatbot: UniversityChatbot, query: str):
    """Handle a single query and exit."""
    result = chatbot.chat(query)

    print("\n" + "="*80)
    print(f"Query: {query}")
    print("="*80)
    print(f"\n{result['response']}")

    if result['universities_found'] > 0:
        print(f"\n📊 Found {result['universities_found']} relevant universities")

    if not result['using_llm']:
        print("\n💡 Tip: Set OPENAI_API_KEY for enhanced LLM responses")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chat with an LLM about universities worldwide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  OPENAI_API_KEY    Your OpenAI API key for LLM responses

Examples:
  # Start interactive chat
  university-chat

  # Ask a single question
  university-chat --query "Tell me about MIT"

  # Show dataset information
  university-chat --stats
        """
    )

    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Ask a single question and exit'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show dataset statistics'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )

    args = parser.parse_args()

    try:
        # Initialize chatbot
        chatbot = UniversityChatbot(api_key=args.api_key)

        if args.stats:
            # Show stats
            print("\n" + "="*80)
            print("UNIVERSITY DATABASE STATISTICS")
            print("="*80)
            print(chatbot.get_statistics_response())

        elif args.query:
            # Single query mode
            single_query_mode(chatbot, args.query)

        else:
            # Interactive mode
            interactive_mode(chatbot)

    except FileNotFoundError:
        print("Error: University dataset not found.")
        print("Please run: python -m ai_native_playground.universities.generate_data")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
