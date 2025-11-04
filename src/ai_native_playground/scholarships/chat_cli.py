"""
Interactive CLI for Scholarship Chatbot

Chat with an LLM to get information about scholarships worldwide.
"""

import argparse
import sys
import os
from pathlib import Path
from .llm_chat import ScholarshipChatbot


def print_header():
    """Print welcome header."""
    print("\n" + "="*80)
    print("💰 SCHOLARSHIP CHATBOT - Powered by LLM + 4000+ Scholarships Dataset")
    print("="*80)


def print_help():
    """Print help information."""
    help_text = """
Available Commands:
  - Type your question to get information about scholarships
  - 'stats' or 'info' - Show dataset statistics
  - 'examples' - Show example queries
  - 'help' - Show this help message
  - 'quit' or 'exit' - Exit the chatbot

Example Questions:
  • "Show me engineering scholarships in the US"
  • "What scholarships are available for graduate students?"
  • "Tell me about Fulbright scholarship"
  • "High-value renewable scholarships"
  • "Scholarships for computer science students"
  • "Need-based scholarships in Canada"
  • "Merit scholarships over $30,000"
"""
    print(help_text)


def print_examples():
    """Print example queries."""
    examples = """
Example Queries to Try:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. By Field of Study:
   • "Show me engineering scholarships"
   • "Scholarships for computer science students"
   • "Medical school scholarships"
   • "Business scholarships for MBA students"

2. By Country/Location:
   • "What scholarships are available in the UK?"
   • "Show me German scholarships"
   • "Scholarships for studying in the United States"
   • "Canadian scholarships for international students"

3. By Amount:
   • "High-value scholarships over $40,000"
   • "Full-ride scholarships"
   • "Scholarships worth more than $50,000"

4. By Type:
   • "Merit-based scholarships"
   • "Need-based financial aid"
   • "Athletic scholarships"
   • "Research scholarships"

5. By Level:
   • "Undergraduate scholarships"
   • "Graduate scholarships for PhD students"
   • "Postdoctoral fellowships"

6. By Characteristics:
   • "Renewable scholarships"
   • "Scholarships with no application fee"
   • "Rolling deadline scholarships"

7. Specific Scholarships:
   • "Tell me about Fulbright scholarship"
   • "What is the Rhodes Scholarship?"
   • "Information about Gates Millennium Scholars"
   • "Details on Chevening Scholarship"
"""
    print(examples)


def interactive_mode(chatbot: ScholarshipChatbot):
    """Run interactive chat mode."""
    print_header()

    if chatbot.llm_available:
        print("✓ Connected to OpenAI GPT-3.5")
        print(f"✓ Loaded {len(chatbot.scholarships):,} scholarships from 18 countries")
    else:
        print("⚠ Running in fallback mode (OpenAI API not configured)")
        print("  For full LLM responses, set: export OPENAI_API_KEY='your-key-here'")
        print(f"✓ Loaded {len(chatbot.scholarships):,} scholarships from 18 countries")

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
                print("\n👋 Thank you for using Scholarship Chatbot!")
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
            if result['scholarships_found'] > 0:
                print(f"\n📊 Retrieved {result['scholarships_found']} scholarships for this response")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


def single_query_mode(chatbot: ScholarshipChatbot, query: str):
    """Handle a single query and exit."""
    result = chatbot.chat(query)

    print("\n" + "="*80)
    print(f"Query: {query}")
    print("="*80)
    print(f"\n{result['response']}")

    if result['scholarships_found'] > 0:
        print(f"\n📊 Found {result['scholarships_found']} relevant scholarships")

    if not result['using_llm']:
        print("\n💡 Tip: Set OPENAI_API_KEY for enhanced LLM responses")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chat with an LLM about scholarships worldwide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  OPENAI_API_KEY    Your OpenAI API key for LLM responses

Examples:
  # Start interactive chat
  scholarship-chat

  # Ask a single question
  scholarship-chat --query "Show me engineering scholarships"

  # Show dataset information
  scholarship-chat --stats
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
        chatbot = ScholarshipChatbot(api_key=args.api_key)

        if args.stats:
            # Show stats
            print("\n" + "="*80)
            print("SCHOLARSHIP DATABASE STATISTICS")
            print("="*80)
            print(chatbot.get_statistics_response())

        elif args.query:
            # Single query mode
            single_query_mode(chatbot, args.query)

        else:
            # Interactive mode
            interactive_mode(chatbot)

    except FileNotFoundError:
        print("Error: Scholarship dataset not found.")
        print("Please run: python -m ai_native_playground.scholarships.generate_scholarships")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
