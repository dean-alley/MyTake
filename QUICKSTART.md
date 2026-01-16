# MyTake Quick Start Guide

**Get up and running with MyTake in 5 minutes.**

---

## Prerequisites

✅ Python 3.9+
✅ Node.js 18+
✅ Anthropic API Key ([get one here](https://console.anthropic.com/))

---

## Installation (First Time)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd MyTake

# 2. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Frontend setup
cd ../frontend
npm install

# Done! 🎉
```

---

## Starting MyTake

**Terminal 1 - Backend:**
```bash
cd backend
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend UI: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## Using MyTake

### Option 1: Web Interface (Easiest)

1. Open http://localhost:5173
2. Paste content or URL in the text area
3. Click "Process"
4. Wait ~6-10 seconds
5. View all 4 sections
6. Click "Sounds like me" / "Doesn't sound like me" to improve

### Option 2: API (For Power Users)

```bash
# Process content
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "Your content here...",
    "source_type": "text"
  }'

# View all processed items
curl http://localhost:8000/api/content | jq .

# Get specific item
curl http://localhost:8000/api/content/1 | jq .

# Submit feedback
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": 1,
    "section": "what_i_say_simple",
    "sounds_like_me": true
  }'
```

---

## Understanding the Output

Every processed item generates **4 sections**:

### 1. What they said — deep
📖 Comprehensive, detailed analysis of the original content
🎯 Perfect for: Understanding nuance and context

### 2. What they said — simple
📄 Clear, concise summary of the original
🎯 Perfect for: Quick reference

### 3. What I'd say — simple
💬 YOUR voice, accessible version
🎯 Perfect for: Casual explanations, sharing with others

### 4. What I'd say — deep
🧠 YOUR voice, thoughtful analysis
🎯 Perfect for: Personal notes, deep engagement

---

## Customizing Your Voice

### Quick Tweaks

Edit `data/voice_profile.json`:

```json
{
  "personality_traits": [
    "curious and questioning",      // Change these
    "pragmatic over theoretical",   // to match
    "values clarity over cleverness" // your style
  ],
  "example_phrases": [
    "Here's what matters:",  // Add phrases
    "The key insight is...", // you actually
    "Worth noting:"          // use
  ]
}
```

### Learning System

The voice profile automatically improves:
- ✅ Mark outputs "Sounds like me" to reinforce good patterns
- ❌ Mark "Doesn't sound like me" to flag issues
- 📝 Add optional feedback text for specifics

---

## Where Files Are Stored

```
data/
├── db.sqlite              # All processed content
├── voice_profile.json     # Your voice configuration
└── docs/                  # Markdown files
    └── 20260116_*.md      # One per processed item
```

**View markdown files:**
```bash
ls -lh data/docs/
cat data/docs/20260116_203856_3_*.md
```

---

## Common Tasks

### View History
```bash
# Via API
curl http://localhost:8000/api/content | jq '.[] | {id, title, created_at}'

# Via frontend
Click "History" tab
```

### Check System Status
```bash
# Health check
curl http://localhost:8000/api/health

# Or use status script
./status.sh
```

### Export Data
```bash
# All markdown files
tar -czf mytake-backup.tar.gz data/docs/

# Database
cp data/db.sqlite backups/db-$(date +%Y%m%d).sqlite

# Voice profile
cp data/voice_profile.json backups/voice-profile-$(date +%Y%m%d).json
```

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Verify API key
cat backend/.env | grep ANTHROPIC_API_KEY

# Check logs
tail -f /tmp/mytake-backend.log
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

### Processing fails
```bash
# Check API health
curl http://localhost:8000/api/health/ai

# Verify model availability
# Edit backend/app/config.py line 23 if needed
```

### YouTube/TikTok not working
- **YouTube**: Requires non-proxied network access
- **TikTok**: Requires Apify API key in `.env`
- **Workaround**: Use text input instead

---

## Tips & Tricks

### Best Practices

✅ **DO:**
- Provide full context (longer text = better results)
- Use feedback buttons to improve voice
- Compare simple vs deep versions
- Export markdown files for long-term storage

❌ **DON'T:**
- Process very short text (< 50 words)
- Expect instant results (allow 5-15 seconds)
- Edit markdown files (they'll be overwritten)
- Share your API key

### Performance

- **Average processing**: 6-10 seconds
- **Longer text**: May take up to 15 seconds
- **API costs**: ~$0.01-0.03 per item (Haiku model)
- **Disk usage**: ~5KB markdown + 48KB database per item

---

## Next Steps

1. **Process your first item** with the web UI
2. **Review the 4 sections** to see voice difference
3. **Provide feedback** on "What I'd say" sections
4. **Check EXAMPLES.md** to see diverse voice examples
5. **Customize voice profile** to match your style

---

## Quick Commands Reference

```bash
# Start backend
cd backend && ./venv/bin/uvicorn app.main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev

# Check status
./status.sh

# Stop everything
./stop.sh

# View all content
curl http://localhost:8000/api/content | jq .

# Process new content
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"input_data": "...", "source_type": "text"}'
```

---

## Getting Help

- **Detailed setup**: See SETUP.md
- **Examples**: See EXAMPLES.md
- **Architecture**: See README.md
- **Deployment**: See DEPLOYMENT_SUMMARY.md
- **Issues**: https://github.com/dean-alley/MyTake/issues

---

**Ready to amplify your thinking? Start processing!** 🚀
