#!/bin/bash

# Setup script for Telegram Bot Scripts
# This script helps configure and run the bot

set -e

echo "🤖 BuildYourSiteProBot Setup"
echo "============================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if BOT_TOKEN is set
if [ -z "$BOT_TOKEN" ]; then
    print_warning "BOT_TOKEN environment variable is not set"
    echo ""
    echo "Please set your bot token:"
    echo ""
    echo "  export BOT_TOKEN=\"8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4\""
    echo ""
    echo "Or enter it now:"
    read -p "Enter BOT_TOKEN: " BOT_TOKEN
    export BOT_TOKEN
fi

print_success "BOT_TOKEN is set (${#BOT_TOKEN} characters)"
echo ""

# Check for Python or Node.js
PYTHON_AVAILABLE=false
NODE_AVAILABLE=false

if command -v python3 &> /dev/null; then
    PYTHON_AVAILABLE=true
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 3 found: $PYTHON_VERSION"
fi

if command -v node &> /dev/null; then
    NODE_AVAILABLE=true
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
fi

if [ "$PYTHON_AVAILABLE" = false ] && [ "$NODE_AVAILABLE" = false ]; then
    print_error "Neither Python 3 nor Node.js found"
    echo "Please install one of them to run the bot"
    exit 1
fi

echo ""
echo "Choose which bot to run:"
echo ""

if [ "$PYTHON_AVAILABLE" = true ]; then
    echo "1) Python Echo Bot (echo-bot.py)"
fi

if [ "$NODE_AVAILABLE" = true ]; then
    echo "2) JavaScript Echo Bot (echo-bot.js)"
fi

echo ""
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ] && [ "$PYTHON_AVAILABLE" = true ]; then
    echo ""
    echo "Checking Python dependencies..."

    if ! python3 -c "import requests" 2>/dev/null; then
        print_warning "requests library not found"
        read -p "Install it now? (y/n): " install_requests
        if [ "$install_requests" = "y" ]; then
            pip3 install requests
            print_success "requests library installed"
        fi
    else
        print_success "requests library is installed"
    fi

    echo ""
    print_success "Starting Python Echo Bot..."
    echo ""
    python3 echo-bot.py

elif [ "$choice" = "2" ] && [ "$NODE_AVAILABLE" = true ]; then
    echo ""
    print_success "Starting Node.js Echo Bot..."
    echo ""
    node echo-bot.js

else
    print_error "Invalid choice or unavailable option"
    exit 1
fi
