# ragebAIt 🔥

**AI Sports Ragebait Generator** — Turn any sports clip into viral-worthy content with AI-powered comedy commentary.

ragebAIt automatically finds the funniest moments in your sports videos, extracts clips, generates hilarious miscommentary using various comedy "lenses" (Nature Documentary, Heist Movie, Shakespearean Drama, etc.), and creates TikTok-ready content complete with voice-over. Then it can auto-post to X (Twitter) via browser automation.

---

## ✨ Features

- 🎬 **Smart Scene Detection** — AI finds the funniest/most viral-worthy moments in your video
- 🎭 **7 Comedy Lenses** — Nature Documentary, Heist Movie, Alien Anthropologist, Cooking Show, Shakespearean Drama, Corporate Meeting, True Crime Podcast
- 🎙️ **AI Voice-Over** — fal.ai TTS with emotion (angry, excited) and adjustable speed for that TikTok energy
- ✂️ **Auto Clip Extraction** — Extracts complete scenes (8-30 seconds) ready for social media
- 🖼️ **Meme Generation** — Create memes from key frames with auto-generated captions
- 🤖 **Auto-Posting** — Browser automation to post directly to X (Twitter)
- 🌐 **Modern Web UI** — Beautiful Next.js frontend with real-time progress

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ragebAIt System                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────┐  │
│  │     Frontend     │    │      Backend     │    │    Browser Auto      │  │
│  │   (Next.js 16)   │───▶│    (FastAPI)     │───▶│  (Browser-Use AI)    │  │
│  │                  │    │                  │    │                      │  │
│  │ • Video Upload   │    │ • Video Analysis │    │ • Auto X Posting     │  │
│  │ • Lens Selection │    │ • Scene Extract  │    │ • Local Chrome       │  │
│  │ • Result Preview │    │ • AI Commentary  │    │ • Gemini-powered     │  │
│  │ • Share Options  │    │ • TTS Generation │    │                      │  │
│  └──────────────────┘    │ • Meme Creation  │    └──────────────────────┘  │
│                          └────────┬─────────┘                              │
│                                   │                                        │
│                    ┌──────────────┴──────────────┐                         │
│                    │       External Services      │                         │
│                    │ • Gemini AI (Video Analysis) │                         │
│                    │ • fal.ai (Text-to-Speech)    │                         │
│                    │ • Vercel Blob (Storage)      │                         │
│                    └─────────────────────────────┘                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ragebAIt/
├── backend/                    # FastAPI backend service
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment configuration
│   ├── models/                 # Pydantic schemas
│   │   └── schemas.py
│   ├── routers/                # API route handlers
│   │   ├── generate.py         # Video generation & commentary
│   │   ├── meme.py             # Meme generation
│   │   └── share.py            # Sharing functionality
│   ├── services/               # Core business logic
│   │   ├── gemini_client.py    # Gemini AI integration
│   │   ├── tts_client.py       # fal.ai TTS integration
│   │   ├── video_processor.py  # OpenCV/MoviePy processing
│   │   ├── storage_client.py   # Vercel Blob storage
│   │   └── meme_engine.py      # Meme rendering
│   ├── prompts/                # AI prompt templates
│   │   └── lenses.py           # Comedy lens definitions
│   └── requirements.txt
│
├── frontend/                   # Next.js web application
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   │   ├── page.tsx        # Home page (upload & generate)
│   │   │   ├── result/         # Result viewing page
│   │   │   └── browser/        # Browser feeds page
│   │   ├── components/         # React components
│   │   │   ├── VideoUploader.tsx
│   │   │   ├── LensSelector.tsx
│   │   │   ├── BrowserFeeds.tsx
│   │   │   └── ui/             # shadcn/ui components
│   │   └── lib/                # Utilities & API client
│   └── package.json
│
├── browser-auto/               # Browser automation for posting
│   ├── main.py                 # CLI entry point
│   ├── poster.py               # Browser-Use agent for X posting
│   ├── requirements.txt
│   └── .env.example
│
└── README.md                   # This file
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async API framework |
| **Gemini AI** | Video analysis & funny moment detection |
| **fal.ai** | Text-to-Speech with emotion |
| **OpenCV** | Video processing |
| **MoviePy** | Audio/video merging |
| **Pillow** | Image processing for memes |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 16** | React framework with App Router |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Utility-first styling |
| **Radix UI** | Accessible UI components |
| **Framer Motion** | Animations |

### Browser Automation
| Technology | Purpose |
|------------|---------|
| **Browser-Use** | AI-powered browser automation |
| **Gemini** | LLM for browser agent decisions |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Chrome (for browser automation)

### 1. Clone the Repository

```bash
git clone https://github.com/abhinavprkash/ragebAIt.git
cd ragebAIt
```

### 2. Backend Setup

```bash
# From the repository root
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
FAL_KEY=your_fal_ai_key_here
VERCEL_BLOB_TOKEN=your_vercel_blob_token  # Optional
DEBUG=true
MOCK_MODE=false
EOF

# Go back to repo root and start the server
cd ..
uvicorn backend.main:app --reload
```

The backend will be available at `http://localhost:8000` with API docs at `/docs`.

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### 4. Browser Automation Setup (Optional)

```bash
cd browser-auto

# Install dependencies with uv (recommended) or pip
uv sync
# or: pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY

# Create a media directory for your content
mkdir -p media

# Run the poster (provide paths to your image and video)
uv run main.py /path/to/your/image.jpg /path/to/your/video.mp4 "Your caption here"
# Or place files in media/ and run interactively:
uv run main.py
```

**Note:** Chrome must be fully closed before running browser automation.

---

## ⚙️ Configuration

### Environment Variables

#### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key for video analysis |
| `FAL_KEY` | ✅ | fal.ai API key for TTS |
| `VERCEL_BLOB_TOKEN` | ❌ | Vercel Blob storage (optional, uses local storage if not set) |
| `DEBUG` | ❌ | Enable debug logging (default: false) |
| `MOCK_MODE` | ❌ | Skip external API calls (default: false) |

#### Browser Automation (`browser-auto/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key for browser agent |

---

## 📡 API Reference

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check with service status |
| `GET` | `/api/lenses` | List available comedy lenses |
| `POST` | `/api/generate` | Generate ragebait clip from video |
| `GET` | `/api/video/{id}` | Get generated video info |

### Meme Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/meme/options` | Get meme options for a video |
| `POST` | `/api/meme/generate` | Generate meme image |

### Generate Ragebait Clip

```bash
curl -X POST http://localhost:8000/api/generate \
  -F "video=@sports_clip.mp4" \
  -F "lens=nature_documentary" \
  -F "min_scene_duration=8" \
  -F "max_scene_duration=30"
```

**Response:**
```json
{
  "video_id": "abc123",
  "video_url": "https://...",
  "thumbnail_url": "https://...",
  "commentary_segments": [
    {
      "start_time": 0.0,
      "end_time": 3.5,
      "text": "BRO WAIT- Look at this guy!",
      "emotion": "excited"
    }
  ],
  "lens": "nature_documentary",
  "duration": 12.5
}
```

---

## 🎭 Comedy Lenses

| Lens | Emoji | Style |
|------|-------|-------|
| `nature_documentary` | 🦁 | David Attenborough observing "homo athleticus" |
| `heist_movie` | 🎬 | Tense thriller narrator ("the package is in play") |
| `alien_anthropologist` | 👽 | Confused alien studying human rituals |
| `cooking_show` | 👨‍🍳 | Enthusiastic chef ("Chef's kiss! That's how you plate a three-pointer!") |
| `shakespearean` | 🎭 | Dramatic tragedy ("But soft! What movement through yonder court breaks?") |
| `corporate_meeting` | 💼 | Business jargon ("synergy", "stakeholders", "quarterly targets") |
| `true_crime` | 🎙️ | Suspenseful podcast ("Here's what they don't want you to know...") |

---

## 🔄 How It Works

1. **Upload** — User uploads a 1-2 minute sports video
2. **Analyze** — Gemini AI watches the video and finds the TOP 3 funniest moments
3. **Extract** — The best scene (highest humor score) is extracted as an 8-30 second clip
4. **Generate** — Ragebait-style commentary is generated using the selected comedy lens
5. **Synthesize** — fal.ai TTS creates voice-over with emotion and 1.2x speed
6. **Merge** — Commentary audio is merged with the clip (original audio lowered)
7. **Share** — Final clip is ready to download or auto-post to X

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run basic tests
python test_api.py

# Test with a video
python test_api.py /path/to/sports_video.mp4
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure nothing is broken
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📝 License

This project is for educational and entertainment purposes.

---

## 🙏 Acknowledgments

- **Google Gemini** for powerful video understanding
- **fal.ai** for high-quality TTS
- **Browser-Use** for AI browser automation
- **Vercel** for hosting and blob storage

---

<p align="center">
  Made with 🔥 for viral sports content
</p>
