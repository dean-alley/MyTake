# MyTake Setup Guide

Complete setup instructions for MyTake.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **Anthropic API key** (get one at https://console.anthropic.com/)
- **Apify API key** (optional, only for TikTok support - get one at https://console.apify.com/)

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd MyTake
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required: ANTHROPIC_API_KEY
# Optional: APIFY_API_KEY (for TikTok)
```

Edit `.env` file:
```
ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
APIFY_API_KEY=your_apify_key_here  # optional
```

### 3. Frontend Setup

```bash
# Open a new terminal window
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

You need to run both backend and frontend:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## Usage

1. **Process a YouTube video:**
   - Paste a YouTube URL into the input field
   - Click "Process"
   - Wait 30-60 seconds for processing
   - View all 4 sections of your MyTake

2. **Process TikTok video:**
   - Ensure you have configured APIFY_API_KEY in .env
   - Paste a TikTok URL
   - Process as normal

3. **Process text directly:**
   - Select "Plain Text" as source type
   - Paste any text content
   - Process as normal

4. **View history:**
   - Click "History" tab to see all processed content
   - Click "View Full Take" on any item to see details

5. **Provide feedback:**
   - On "What I'd say" sections, you can mark if it sounds like you
   - This helps improve your voice profile over time

## Voice Profile Customization

Your voice profile is stored in `data/voice_profile.json`. You can:

1. View the current profile:
```bash
cat data/voice_profile.json
```

2. Edit manually to adjust your voice characteristics:
   - Tone and style preferences
   - Phrases you commonly use
   - Things to avoid

3. The profile evolves automatically based on your feedback

## Data Storage

All data is stored locally:

- **Database**: `data/db.sqlite`
- **Markdown files**: `data/docs/`
- **Voice profile**: `data/voice_profile.json`

## Troubleshooting

### Backend won't start

1. Check Python version: `python --version` (should be 3.9+)
2. Ensure virtual environment is activated
3. Verify API key is set in `.env`
4. Check logs for specific errors

### Frontend won't start

1. Check Node version: `node --version` (should be 18+)
2. Delete `node_modules` and run `npm install` again
3. Check if port 5173 is already in use

### API Key errors

1. Verify your Anthropic API key is valid
2. Check that `.env` file exists and is in the `backend/` directory
3. Restart the backend server after changing `.env`

### YouTube extraction fails

- Some videos may not have transcripts available
- Check if the video is public and has captions
- Try a different video to verify the system works

### TikTok extraction fails

- Ensure APIFY_API_KEY is configured
- Verify the Apify actor ID is correct in `backend/app/extractors/tiktok.py`
- Some TikTok videos may be private or region-restricted

## Development

### Backend Tests

```bash
cd backend
pytest
```

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

### Database Reset

To start fresh:

```bash
rm data/db.sqlite
rm data/voice_profile.json
rm -rf data/docs/*
```

The database and default voice profile will be recreated on next startup.

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in `.env`
2. Use a production ASGI server (Gunicorn + Uvicorn)
3. Set up proper CORS origins
4. Consider using PostgreSQL instead of SQLite
5. Set up reverse proxy (nginx)
6. Enable HTTPS

See `DEPLOYMENT.md` (coming soon) for detailed production setup.

## Support

- **Issues**: Report bugs or request features on GitHub
- **Documentation**: See `README.md` for architecture overview
- **API Reference**: http://localhost:8000/docs when running

## License

MIT License - see LICENSE file
