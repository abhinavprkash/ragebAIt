# ragebAIt 🔥

AI-powered sports ragebait generator. Upload a sports video, and the AI will find the funniest moment, extract it as a complete scene, add viral "ragebait" commentary, and generate a meme - all ready for TikTok/Twitter.

## Features

- **🎯 Smart Scene Detection**: Uses Gemini to find the funniest moments and extracts complete scenes (not arbitrary cuts)
- **🎙️ Ragebait Commentary**: Generates fast-paced, angry TikTok-style narration using fal.ai TTS
- **🎭 Multiple Commentary Styles**: Nature Documentary, Heist Movie, Alien Anthropologist, Cooking Show, Shakespeare, Corporate, True Crime
- **🍌 Nano Banana Memes**: AI-generated gen-z sports memes using Gemini's native image generation
- **⚡ Full Pipeline**: Upload → Scene Detection → Clip Extraction → Commentary → TTS → Final Video

## Tech Stack

**Backend:**
- FastAPI + Python
- Gemini 3 Flash (video analysis & commentary)
- fal.ai TTS (ragebait voice synthesis)
- Gemini Pro Image (meme generation)
- Vercel Blob Storage

**Frontend:**
- Next.js 16 + React 19
- Tailwind CSS + shadcn/ui
- Framer Motion
- Sonner (toasts)

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv ../venv
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-gemini-api-key"
export FAL_KEY="your-fal-ai-key"
export BLOB_READ_WRITE_TOKEN="your-vercel-blob-token"  # Optional

# Run from project root
cd ..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run dev server
npm run dev
```

### 3. Test the API

```bash
python backend/test_api.py videos/test.mp4
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/lenses` | List available commentary styles |
| `POST` | `/api/generate` | Upload video & generate ragebait clip |
| `GET` | `/api/video/{id}` | Get video info & transcript |
| `POST` | `/api/meme/generate` | Generate meme from video frame |
| `GET` | `/api/meme/styles` | List available meme styles |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `FAL_KEY` | ✅ | fal.ai API key for TTS |
| `BLOB_READ_WRITE_TOKEN` | ⬜ | Vercel Blob Storage token |
| `GOOGLE_CLOUD_PROJECT` | ⬜ | GCP project (optional, for Vertex AI) |

## How It Works

1. **Upload**: User uploads a 1-2 minute sports video
2. **Scene Detection**: Gemini analyzes the video and finds the funniest complete scene
3. **Clip Extraction**: The scene is extracted (8-30 seconds, capturing the full action)
4. **Commentary Generation**: Gemini writes ragebait-style commentary for the clip
5. **TTS Synthesis**: fal.ai generates angry, fast-paced TikTok voice
6. **Audio Merge**: Commentary is mixed with original audio (lowered)
7. **Meme Generation**: Nano Banana creates a gen-z meme from the best frame

## License

MIT
