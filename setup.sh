#!/bin/bash

# Professional Trading Dashboard Setup Script
# Compatible with Termux and Linux

echo "====================================="
echo "Crypto Trading Dashboard Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[✓] Python3 found: $(python3 --version)"
echo ""

# Create virtual environment (optional but recommended)
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[✓] Virtual environment created"
echo ""

# Install requirements
echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "[✓] All dependencies installed successfully!"
else
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit main.py and add your Binance API keys"
echo "2. Get keys from: https://www.binance.com/en/account/api-management"
echo "3. Run: python main.py"
echo ""
echo "For WebSocket version (real-time):"
echo "   python websocket_version.py"
echo ""
echo "To deactivate virtual environment:"
echo "   deactivate"
echo ""
