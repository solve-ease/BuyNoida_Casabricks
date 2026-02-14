#!/bin/bash
# Startup script for CasaBricks Backend

set -e

echo "======================================"
echo "CasaBricks Backend Startup"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please copy .env.backend.example to .env and configure it"
    exit 1
fi

echo "✓ Environment file found"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv package manager not found!"
    echo "   Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv package manager found"

# Install/update dependencies
echo ""
echo "Installing dependencies..."
uv sync

echo "✓ Dependencies installed"

# Check if Redis is running
echo ""
echo "Checking Redis connection..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Warning: Redis is not running!"
    echo "   Some features may not work. Start Redis with: redis-server"
else
    echo "✓ Redis is running"
fi

# Run migrations
echo ""
echo "Running database migrations..."
uv run alembic upgrade head
echo "✓ Migrations complete"

# Start the server
echo ""
echo "======================================"
echo "Starting server..."
echo "======================================"
echo ""
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "Metrics: http://localhost:8000/metrics"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
