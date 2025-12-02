#!/bin/bash

# HyperOPS Trading System Setup Script

echo "🚀 Setting up HyperOPS Trading System..."
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.8+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create config directory
echo "📁 Creating config directory..."
mkdir -p config
mkdir -p research_logs

# Create sample configuration
echo "⚙️ Creating sample configuration..."
python3 -c "from trading_module import create_sample_config; create_sample_config()"

# Make CLI executable
echo "🔧 Making CLI executable..."
chmod +x hyperops_cli.py

# Create symlink for easy access (optional)
echo "🔗 Creating symlink..."
ln -sf "$(pwd)/hyperops_cli.py" /usr/local/bin/hyperops 2>/dev/null || echo "⚠️  Could not create system symlink (requires sudo)"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit config/trading_config.json.example with your credentials"
echo "2. Rename to config/trading_config.json"
echo "3. Run tests: python3 test_trading_system.py"
echo "4. Start trading: python3 hyperops_cli.py session"
echo ""
echo "For help: python3 hyperops_cli.py --help"