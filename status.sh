#!/bin/bash
# MyTake Status Script
# Checks the status of all MyTake components

echo "📊 MyTake System Status"
echo "======================="
echo ""

# Check backend
echo "Backend Server (port 8000):"
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    STATUS=$(curl -s http://localhost:8000/api/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    echo "  ✅ Running - Status: $STATUS"
    echo "  🔗 http://localhost:8000"
else
    echo "  ❌ Not running or unhealthy"
fi
echo ""

# Check frontend
echo "Frontend Server (port 5173):"
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "  ✅ Running"
    echo "  🔗 http://localhost:5173"
else
    echo "  ❌ Not running"
fi
echo ""

# Check Claude AI connectivity
echo "Claude AI Connection:"
AI_STATUS=$(curl -s http://localhost:8000/api/health/ai 2>/dev/null)
if echo "$AI_STATUS" | grep -q '"ready":true'; then
    echo "  ✅ Connected and ready"
elif echo "$AI_STATUS" | grep -q '"ready":false'; then
    echo "  ⚠️  Backend running but AI check failed"
else
    echo "  ❌ Cannot check (backend not running)"
fi
echo ""

# Check database
echo "Database:"
if [ -f "data/db.sqlite" ]; then
    DB_SIZE=$(du -h data/db.sqlite | cut -f1)
    echo "  ✅ Found (size: $DB_SIZE)"

    # Count content items
    CONTENT_COUNT=$(curl -s http://localhost:8000/api/content 2>/dev/null | grep -o '"id":' | wc -l)
    if [ "$CONTENT_COUNT" -gt 0 ]; then
        echo "  📄 Content items: $CONTENT_COUNT"
    fi
else
    echo "  ⚠️  Database not found (will be created on first run)"
fi
echo ""

# Check voice profile
echo "Voice Profile:"
if [ -f "data/voice_profile.json" ]; then
    echo "  ✅ Found"
    UPDATED=$(grep '"updated_at"' data/voice_profile.json | cut -d'"' -f4 | cut -dT -f1)
    echo "  📅 Last updated: $UPDATED"
else
    echo "  ⚠️  Not found (will be created on first run)"
fi
echo ""

# Check markdown docs
echo "Generated Documents:"
if [ -d "data/docs" ]; then
    DOC_COUNT=$(ls -1 data/docs/*.md 2>/dev/null | wc -l)
    if [ "$DOC_COUNT" -gt 0 ]; then
        echo "  ✅ $DOC_COUNT markdown file(s)"
        TOTAL_SIZE=$(du -sh data/docs 2>/dev/null | cut -f1)
        echo "  💾 Total size: $TOTAL_SIZE"
    else
        echo "  ℹ️  No documents yet"
    fi
else
    echo "  ⚠️  Docs directory not found"
fi
echo ""

# System health summary
echo "======================="
if curl -s http://localhost:8000/api/health > /dev/null 2>&1 && lsof -ti:5173 > /dev/null 2>&1; then
    echo "✅ System Status: HEALTHY"
    echo ""
    echo "Ready to process content at http://localhost:5173"
else
    echo "⚠️  System Status: PARTIAL"
    echo ""
    echo "Run ./start.sh to start MyTake"
fi
