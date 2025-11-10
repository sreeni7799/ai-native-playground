#!/bin/bash
#
# Daily Digest Script
#
# Combines weather, news, tasks, and optionally scholarship/university updates
# into a single daily report.
#
# Usage:
#   ./daily_digest.sh [city] [country]
#
# Examples:
#   ./daily_digest.sh Boston "United States"
#   ./daily_digest.sh London
#   ./daily_digest.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
CITY="${1:-Boston}"
COUNTRY="${2:-United States}"
WEATHER_API_URL="http://localhost:8000"
MAX_NEWS=5

# Check if running in color-supported terminal
if [ -t 1 ]; then
    USE_COLOR=1
else
    USE_COLOR=0
fi

# Helper functions
print_header() {
    echo ""
    echo "========================================================================"
    echo "  $1"
    echo "========================================================================"
    echo ""
}

print_section() {
    echo ""
    if [ $USE_COLOR -eq 1 ]; then
        echo -e "${CYAN}$1${NC}"
    else
        echo "$1"
    fi
    echo "------------------------------------------------------------------------"
}

# Main digest
clear
print_header "📅 DAILY DIGEST - $(date '+%A, %B %d, %Y')"

# ============================================================================
# WEATHER
# ============================================================================
print_section "🌤️  Weather Forecast"

# Check if weather API is running
if curl -s "$WEATHER_API_URL/current?city=$CITY" > /dev/null 2>&1; then
    weather_data=$(curl -s "$WEATHER_API_URL/current?city=$CITY")

    temp=$(echo "$weather_data" | jq -r '.temperature // "N/A"')
    feels_like=$(echo "$weather_data" | jq -r '.feels_like // "N/A"')
    weather=$(echo "$weather_data" | jq -r '.weather_main // "N/A"')
    description=$(echo "$weather_data" | jq -r '.weather_description // "N/A"')
    humidity=$(echo "$weather_data" | jq -r '.humidity // "N/A"')

    echo "Location: $CITY"
    echo "Temperature: ${temp}°F (Feels like: ${feels_like}°F)"
    echo "Conditions: $weather - $description"
    echo "Humidity: ${humidity}%"
else
    echo "⚠️  Weather API not running (start with: weather-api)"
    echo "   Run 'weather-api' in a separate terminal to enable weather updates"
fi

# ============================================================================
# NEWS
# ============================================================================
print_section "📰 Top Tech News"

if command -v news-analyzer &> /dev/null; then
    news-analyzer --quick --max-headlines $MAX_NEWS 2>/dev/null | head -30
else
    echo "⚠️  News analyzer not available"
    echo "   Install with: pip install -e ."
fi

# ============================================================================
# TASKS
# ============================================================================
print_section "✅ Today's Tasks"

if command -v todo-app &> /dev/null; then
    task_count=$(todo-app list 2>/dev/null | wc -l)

    if [ $task_count -gt 0 ]; then
        todo-app list 2>/dev/null
        echo ""
        echo "Total tasks: $task_count"
    else
        echo "No tasks for today! 🎉"
        echo ""
        echo "Add tasks with: todo-app add \"Your task here\""
    fi
else
    echo "⚠️  Todo app not available"
    echo "   Install with: pip install -e ."
fi

# ============================================================================
# OPTIONAL: SCHOLARSHIP UPDATES
# ============================================================================
if [ "$3" == "--scholarships" ]; then
    print_section "💰 New Scholarship Opportunities"

    if command -v scholarship-recommend &> /dev/null; then
        echo "High-value renewable scholarships:"
        scholarship-recommend --min-amount 30000 --renewable --n 5 2>/dev/null | \
            grep -E "(^\s*[0-9]+\.|Amount:|Provider:|Country:)" | head -25
    else
        echo "⚠️  Scholarship tools not available"
    fi
fi

# ============================================================================
# OPTIONAL: UNIVERSITY UPDATES
# ============================================================================
if [ "$3" == "--universities" ]; then
    print_section "🎓 Top Universities in $COUNTRY"

    if command -v universities &> /dev/null; then
        universities --country "$COUNTRY" --limit 5 2>/dev/null | head -25
    else
        echo "⚠️  University tools not available"
    fi
fi

# ============================================================================
# QUICK STATS
# ============================================================================
print_section "📊 Quick Stats"

echo "Date: $(date '+%Y-%m-%d')"
echo "Time: $(date '+%H:%M:%S')"
echo "Day of Year: $(date '+%j')/365"
echo "Week: $(date '+%U')"

# System info
if command -v uptime &> /dev/null; then
    echo ""
    echo "System uptime: $(uptime -p 2>/dev/null || uptime)"
fi

# ============================================================================
# REMINDERS
# ============================================================================
print_section "💡 Reminders"

echo "• Don't forget to check your emails"
echo "• Review your application deadlines"
echo "• Stay hydrated! 💧"

# ============================================================================
# FOOTER
# ============================================================================
echo ""
echo "========================================================================"
echo "  Have a productive day! 🚀"
echo "========================================================================"
echo ""

# Usage tips
if [ "$3" != "--help" ]; then
    echo "💡 Pro Tips:"
    echo "   • Run with --scholarships to include scholarship updates"
    echo "   • Run with --universities to include university info"
    echo "   • Schedule daily: Add to crontab with 'crontab -e'"
    echo "   • Example cron: 0 8 * * * /path/to/daily_digest.sh Boston \"United States\""
    echo ""
fi
