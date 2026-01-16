#!/bin/bash
# MyTake Startup Script
# Starts both backend and frontend servers

set -e

echo "🚀 Starting MyTake..."
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the MyTake root directory"
    exit 1
fi

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Error: Backend virtual environment not found"
    echo "Please run: cd backend && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Error: Frontend dependencies not installed"
    echo "Please run: cd frontend && npm install"
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: Backend .env file not found"
    echo "Please copy backend/.env.example to backend/.env and configure your API keys"
    exit 1
fi

echo "✅ Pre-flight checks passed"
echo ""

# Start backend
echo "🔧 Starting backend server..."
cd backend
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/mytake-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend running at http://localhost:8000"
else
    echo "❌ Backend failed to start. Check logs: tail -f /tmp/mytake-backend.log"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev > /tmp/mytake-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 3

echo ""
echo "✅ MyTake is running!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:   tail -f /tmp/mytake-backend.log"
echo "   Frontend:  tail -f /tmp/mytake-frontend.log"
echo ""
echo "🛑 To stop MyTake, run: ./stop.sh"
echo ""
echo "Backend PID: $BACKEND_PID" > .mytake-pids
echo "Frontend PID: $FRONTEND_PID" >> .mytake-pids

echo "Happy processing! 🎯"
