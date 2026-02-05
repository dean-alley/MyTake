# MyTake

**MyTake is a local-first tool for digesting content and re-expressing it in my own voice. Paste a link, get understanding — not just a summary.**

> 📖 **New here?** Check out [SETUP.md](SETUP.md) for detailed setup instructions and troubleshooting.

## What MyTake Is

MyTake is a personal content digestion tool that turns links into understanding and re-expression — in your voice, at low effort.

Not a content farm.
Not a notes app.
**A thinking amplifier.**

## Core Features

### Input
- Paste URL (YouTube / TikTok via Apify)
- Or paste text (fallback / quick mode)

### Auto-processing
1. Extract transcript/text
2. Run Claude with voice profile + fixed 4-part schema
3. Save results

### Output (always generated)
1. **What they said — deep**: Comprehensive analysis of the original content
2. **What they said — simple**: Accessible summary of the original content
3. **What I'd say — simple**: Your voice, accessible version
4. **What I'd say — deep**: Your voice, comprehensive version

### Persistence
- Local `.md` file saved alongside DB record
- Google Doc integration (coming soon)

## Voice System

MyTake's "voice" is not training a model. It's:
- A versioned voice profile (JSON)
- Built from:
  - Style rules
  - Preferences
  - Your feedback
  - Accumulated "good outputs"
- Injected into every Claude call

This means:
- You can tweak it
- You can diff it
- You can intentionally evolve it

No black box. No magic. Just control.

### Voice Profile v2.0: Content Creation Framework

The voice profile now supports a richer framework for content creation through **reaction and reframing**:

**Core Philosophy**: You don't create content from scratch - you create content through reaction and reframing. Your best insights come when you encounter something that resonates, then process it through your unique lens.

**New Profile Features**:
- **Unique Filters**: Define your perspective lenses (e.g., "The AI-First Practitioner", "The Working Creative")
- **Processing Questions**: Questions to run content through ("What's my lived experience with this?")
- **Content Sweet Spots**: Topics where your voice shines
- **Voice Markers**: Authentic expressions and speech patterns
- **Background Context**: Lived experience for grounding responses

See `backend/voice_profile.example.json` for a complete example of the v2.0 profile format.

## Architecture

### Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **AI**: Anthropic Claude
- **Storage**: SQLite + Local Markdown
- **External Services**: Apify (for TikTok), YouTube API

### Directory Structure

```
mytake/
├─ backend/
│  ├─ app/
│  │  ├─ main.py            # FastAPI entry
│  │  ├─ api/               # routes
│  │  ├─ workers/           # Apify + AI jobs
│  │  ├─ extractors/        # YouTube / TikTok
│  │  ├─ ai/                # Claude client + prompts
│  │  ├─ voice/             # voice_profile logic
│  │  └─ storage/           # SQLite + files
│  ├─ requirements.txt
│
├─ frontend/
│  ├─ src/
│  └─ vite.config.ts
│
├─ data/
│  ├─ docs/                 # markdown backups
│  └─ db.sqlite
│
├─ README.md
└─ docker-compose.yml       # later
```

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Anthropic API key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:

```
ANTHROPIC_API_KEY=your_api_key_here
APIFY_API_KEY=your_apify_key_here  # optional, for TikTok
```

Run the backend:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Open the web interface (typically `http://localhost:5173`)
2. Paste a YouTube or TikTok URL (or raw text)
3. Click "Process"
4. MyTake automatically generates all 4 sections
5. View results and access the saved Markdown file

## Roadmap

### MVP (Current)
- [x] YouTube transcript extraction
- [x] Claude AI integration with 4-part output
- [x] Voice profile system
- [x] Local Markdown storage
- [x] SQLite database
- [x] Basic web UI

### Next Steps
- [x] Apify TikTok integration
- [x] "Sounds like me / doesn't sound like me" feedback button
- [x] Voice profile evolution based on feedback
- [x] Text-only quick mode
- [ ] Google Docs integration (placeholder ready)

### Future
- [ ] Docker containerization
- [ ] LAN hosting mode
- [ ] Voice profile versioning UI
- [ ] Export to multiple formats

## Philosophy

MyTake is:
- **Local-first**: Your data stays with you
- **Transparent**: No black-box AI, configurable voice profiles
- **Purposeful**: Built to amplify thinking, not replace it
- **Personal**: It learns YOUR voice, not a generic one

## License

MIT
