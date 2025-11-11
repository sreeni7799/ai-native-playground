#!/bin/bash
# Render build script for AI Education Platform
# This script ensures dependencies are installed in the correct order

set -e  # Exit on error

echo "========================================="
echo "🚀 Building AI Education Platform"
echo "========================================="

# Step 1: Upgrade pip
echo ""
echo "📦 Step 1: Upgrading pip..."
pip install --upgrade pip

# Step 2: Install dependencies from requirements.txt
echo ""
echo "📦 Step 2: Installing dependencies..."
pip install -r requirements.txt

# Step 3: Install package in editable mode
echo ""
echo "📦 Step 3: Installing package..."
pip install -e .

# Step 4: Generate university data
echo ""
echo "🎓 Step 4: Generating university dataset (4,550 universities)..."
python -m ai_native_playground.universities.generate_4000_data

# Step 5: Generate scholarship data
echo ""
echo "💰 Step 5: Generating scholarship dataset (4,011 scholarships)..."
python -m ai_native_playground.scholarships.generate_scholarships

echo ""
echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="
echo ""
echo "Platform includes:"
echo "  ✓ 4,550 universities across 20 countries"
echo "  ✓ 4,011 scholarships across 18 countries"
echo "  ✓ ML recommendation models"
echo "  ✓ AI chatbot with RAG"
echo ""
