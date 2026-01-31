# Backend Integration Guide for ragebAIt

This document outlines the API endpoints the Frontend expects from the Backend (FastAPI).

## Base URL
`http://localhost:8000` (Local)
`https://api.ragebait.com` (Production)

---

## 1. Upload & Generate Roast
**Endpoint:** `POST /api/generate`

**Request:** `multipart/form-data`
- `file`: Video file (mp4, mov) OR Image file (jpg, png)
- `lens_id`: String (e.g., "roast_master", "nature_doc")

**Response:**
```json
{
  "job_id": "12345-abcde",
  "status": "processing",
  "eta_seconds": 15
}
```

---

## 2. Check Result / Get Analysis
**Endpoint:** `GET /api/result/{job_id}`

**Response:**
```json
{
  "id": "12345-abcde",
  "status": "completed", // "processing", "failed"
  "video_url": "https://storage.googleapis.com/.../processed.mp4",
  "transcript": [
    { "timestamp": "00:02", "text": "Look at that stance!" },
    { "timestamp": "00:05", "text": "Elbows in!" }
  ],
  "meme_url": "https://fal.ai/.../meme.png" // Optional initial meme
}
```

---

## 3. Live Browser Feeds (For Right Sidebar)
**Endpoint:** `GET /api/browser-feeds`

**Response:**
```json
{
  "feeds": [
    {
      "id": "1",
      "source": "twitter",
      "user": "@NBAMemes",
      "content": "LeBron just missed a dunk...",
      "timestamp": "2023-10-27T10:00:00Z"
    },
    {
      "id": "2",
      "source": "news",
      "user": "ESPN",
      "content": "Mahomes injury update...",
      "timestamp": "2023-10-27T09:45:00Z"
    }
  ]
}
```
**Owner:** Sanskar (Browser Use Agent)

---

## 4. Generate Meme (Interactive)
**Endpoint:** `POST /api/meme/generate`

**Request:** `application/json`
```json
{
  "video_id": "12345-abcde",
  "caption": "When you try to impress your crush...",
  "format": "square" // "portrait", "landscape"
}
```

**Response:**
```json
{
  "meme_url": "https://fal.ai/.../new_meme.png"
}
```
**Owner:** Dizzy (Nano Banana / Flux)

---

## Team Responsibilities
- **Frontend (Vatsala):** Consumes these APIs.
- **Backend (Abhinav):** Implements `/api/generate` and `/api/result` (Gemini + TTS).
- **Meme Agent (Dizzy):** Implements `/api/meme/generate`.
- **Browser Agent (Sanskar):** Feeds data into `/api/browser-feeds`.
