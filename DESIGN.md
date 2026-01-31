# Social Media Manager AI Agent — MVP Design

## Overview
CLI tool that watches a local folder for images/videos, uses Gemini to generate funny captions, shows them for human approval, then uses browser-use to post to X.

## Architecture
```
 ./media/          Gemini API         Terminal          browser-use         X (Twitter)
 ┌──────┐        ┌───────────┐      ┌────────┐       ┌───────────┐      ┌──────────┐
 │image/ │──────▶│ Analyze &  │─────▶│ Show   │──────▶│ Open X,   │─────▶│ Published│
 │video  │       │ Caption    │      │ Approve│       │ Upload &  │      │ Post     │
 └──────┘        └───────────┘      └────────┘       │ Post      │      └──────────┘
                                        │             └───────────┘
                                     [Edit/Skip]
```

## Project Structure
```
GeminiHackathon2026/
├── main.py              # Entry point — orchestrates the full flow
├── caption.py           # Gemini API: analyze media → generate caption
├── poster.py            # browser-use: post media + caption to X
├── requirements.txt     # Dependencies
├── .env.example         # Template for API keys
├── DESIGN.md            # This file
└── media/               # Drop images/videos here (created at runtime)
    └── posted/          # Successfully posted files moved here
```

## Flow
```
1. Scan ./media/ for new image/video files
2. For each file:
   a. Send to Gemini → get funny caption
   b. Print caption to terminal, ask user: [Y]es / [E]dit / [S]kip
   c. If approved → browser-use agent posts to X with the file + caption
   d. On success → move file to ./media/posted/
3. Exit when all files processed
```

## File Details

### `main.py` (~60 lines)
Entry point. Scans `./media/` for supported files and orchestrates the caption → approve → post loop.

- Supported formats: `.jpg`, `.png`, `.gif`, `.webp`, `.mp4`, `.mov`
- Creates `./media/` and `./media/posted/` dirs if missing
- Loop through each file:
  - Call `caption.generate_caption(filepath)` → get caption string
  - Print caption, prompt user: `[Y]es / [E]dit / [S]kip`
  - Call `poster.post_to_x(filepath, caption)` → post via browser-use
  - On success, move file to `./media/posted/`
- Uses `asyncio.run()` as entry point

### `caption.py` (~30 lines)
Handles Gemini API calls for caption generation.

- `generate_caption(filepath: str) -> str`
- Images: load via PIL, pass directly to Gemini
- Videos: use Gemini's File API to upload first
- API call:
  ```python
  from google import genai
  client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[media, PROMPT]
  )
  ```
- System prompt: *"You are a witty social media manager. Generate a short, funny, viral-worthy caption for this image/video to post on X (Twitter). Keep it under 280 characters. Just return the caption text, nothing else."*

### `poster.py` (~40 lines)
Handles browser automation to post on X.

- `async post_to_x(filepath: str, caption: str) -> bool`
- Uses persistent browser profile so X login is remembered across runs:
  ```python
  browser = Browser(
      headless=False,
      user_data_dir="~/.config/browseruse/profiles/x-poster",
  )
  agent = Agent(
      task=f"Go to x.com. Create a new post with this text: '{caption}'. "
           f"Upload the file at '{abs_path}' as media attachment. "
           f"Then click the Post button to publish it.",
      llm=ChatBrowserUse(),
      browser=browser,
      use_vision=True,
      max_steps=25,
  )
  ```
- Returns `True`/`False` based on success
- Cleans up browser in `finally` block

## Dependencies

### `requirements.txt`
```
browser-use
google-genai
python-dotenv
Pillow
```

### `.env.example`
```
GEMINI_API_KEY=your-gemini-api-key
BROWSER_USE_API_KEY=your-browser-use-api-key
```

## How to Run
```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Copy and fill in API keys
cp .env.example .env

# 3. Drop images/videos into ./media/ folder

# 4. Run (first run: log into X manually in the browser that opens)
python main.py
```

On first run, browser-use will open a visible browser. Log into X manually — the session persists for future runs via the browser profile directory.

## Verification
1. Place a test image in `./media/`
2. Run `python main.py`
3. Confirm a caption is generated and printed to terminal
4. Approve the caption (type `y`)
5. Watch the browser open, navigate to X, and post
6. Verify the file moved to `./media/posted/`
7. Check X to confirm the post appeared with correct caption + media
