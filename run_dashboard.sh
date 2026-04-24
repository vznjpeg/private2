#!/bin/bash

echo "🚀 Market Growth & Revenue Analyzer Dashboard"
echo "=============================================="
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✓ Starting dashboard server..."
echo ""
echo "📱 Dashboard: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
