#!/bin/bash
# Home Services Lead Machine — Dependency Installer
#
# Run this from the automation/ directory:
#   cd automation && bash scripts/setup.sh

echo ""
echo "=== Home Services Lead Machine — Setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found."
    echo "Install it from: https://www.python.org/downloads/"
    exit 1
fi

echo "Python: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate
echo "Virtual environment activated"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright Chromium browser..."
playwright install chromium

# Create directories
echo "Creating data directories..."
mkdir -p data logs profiles/craigslist profiles/facebook screenshots
mkdir -p craigslist/ad_templates/images

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env with your info, or run: python ../setup/wizard.py"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run the setup wizard:  python ../setup/wizard.py"
echo "     (or edit .env and config/settings.yaml manually)"
echo ""
echo "  2. Test your proxy:       python scripts/test_proxy.py"
echo "  3. Test CL posting:       python craigslist/poster.py --test"
echo "  4. Check ad status:       python craigslist/poster.py --status"
echo "  5. Verify ads are live:   python craigslist/ghost_check.py --search"
echo ""
echo "Or just open this repo in Claude Code and say 'set me up'"
echo ""
