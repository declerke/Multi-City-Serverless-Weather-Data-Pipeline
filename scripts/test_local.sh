#!/bin/bash

echo "🧪 Testing Weather Alert System Locally"
echo "========================================"

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

source .env

echo ""
echo "📍 Testing for: $CITY_NAME ($LAT, $LON)"
echo ""

cd "$(dirname "$0")/.."

export PYTHONPATH="${PYTHONPATH}:./src"

python tests/test_local.py \
    --lat $LAT \
    --lon $LON \
    --city "$CITY_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Local test passed successfully"
else
    echo ""
    echo "❌ Local test failed"
    exit 1
fi