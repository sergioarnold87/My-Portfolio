#!/bin/bash

echo "🧠 RAG Demo - Data Engineering Discovery Assistant"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    cp .env.template .env
    echo -e "${GREEN}✓${NC} .env file created from template"
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANT: Edit .env file and add your OpenAI API key!${NC}"
    echo "   Run: nano .env"
    echo "   Or use local LLM (see README.md for instructions)"
else
    echo -e "${YELLOW}⚠ .env file already exists. Skipping creation.${NC}"
fi

# Verify data files
echo ""
echo "📚 Verifying knowledge base..."
data_count=$(ls -1 data/*.txt 2>/dev/null | wc -l)
if [ $data_count -eq 6 ]; then
    echo -e "${GREEN}✓${NC} All 6 knowledge base files found"
else
    echo -e "${RED}❌ Warning: Expected 6 data files, found $data_count${NC}"
fi

# Summary
echo ""
echo "=================================================="
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env file and add your API key:"
echo "      nano .env"
echo ""
echo "   2. Activate virtual environment (if not already active):"
echo "      source venv/bin/activate"
echo ""
echo "   3. Run the application:"
echo "      streamlit run app/main.py"
echo ""
echo "📖 For more information, see README.md or QUICKSTART.md"
echo "=================================================="
