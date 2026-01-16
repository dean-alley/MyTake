#!/bin/bash
# MyTake Stop Script
# Stops both backend and frontend servers

echo "🛑 Stopping MyTake..."
echo ""

# Stop backend on port 8000
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "Stopping backend server..."
    fuser -k 8000/tcp 2>/dev/null || kill $(lsof -ti:8000) 2>/dev/null || true
    echo "✅ Backend stopped"
else
    echo "ℹ️  Backend not running"
fi

# Stop frontend on port 5173
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "Stopping frontend server..."
    fuser -k 5173/tcp 2>/dev/null || kill $(lsof -ti:5173) 2>/dev/null || true
    echo "✅ Frontend stopped"
else
    echo "ℹ️  Frontend not running"
fi

# Clean up PID file
if [ -f ".mytake-pids" ]; then
    rm .mytake-pids
fi

echo ""
echo "✅ MyTake stopped successfully"
