"""
ragebAIt - Meme Generation Router
Handles meme generation using Nano Banana (Gemini's native image generation).
"""

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.config import settings
from backend.services.meme_engine import meme_engine
from backend.services.storage_client import storage_client
from backend.routers.generate import get_video_data


router = APIRouter(tags=["meme"])


class MemeGenerateRequest(BaseModel):
    """Request to generate a meme from a video frame."""
    video_id: str = Field(..., description="Video ID to get frame from")
    frame_index: Optional[int] = Field(default=None, description="Specific frame index (default: best frame)")


class MemeGenerateResponse(BaseModel):
    """Response with generated meme."""
    meme_id: str = Field(..., description="Unique meme ID")
    meme_url: str = Field(..., description="URL to generated meme image")
    caption: str = Field(..., description="Social media caption with hashtags")
    style: str = Field(..., description="Meme style used")
    image_prompt: str = Field(..., description="The prompt used to generate the meme")


# In-memory store for meme data (mirrors video_store pattern)
# In production, use Redis or database
meme_store: dict[str, dict] = {}

@router.post(
    "/api/meme/generate",
    response_model=MemeGenerateResponse,
    summary="Generate a gen-z meme from video frame"
)
async def generate_meme(request: MemeGenerateRequest):
    """
    Generate a gen-z sports meme using Nano Banana (Gemini's native image generation).
    
    This endpoint:
    1. Takes a frame from a previously processed video
    2. Analyzes it for meme potential
    3. Uses Nano Banana to generate a styled meme
    4. Returns the meme with a social media caption
    
    Styles include: deepfried, surreal, wholesome, cursed, clean, chaotic
    """
    if not meme_engine.is_available():
        raise HTTPException(
            status_code=503,
            detail="Nano Banana meme engine not available. Check GOOGLE_CLOUD_PROJECT or GEMINI_API_KEY."
        )
    
    # Get video data
    video_data = get_video_data(request.video_id)
    if not video_data:
        raise HTTPException(status_code=404, detail="Video not found")
    
    frames = video_data.get("frames", [])
    if not frames:
        raise HTTPException(status_code=404, detail="No frames available for this video")
    
    # Select frame
    if request.frame_index is not None:
        if request.frame_index < 0 or request.frame_index >= len(frames):
            raise HTTPException(status_code=400, detail=f"Frame index out of range (0-{len(frames)-1})")
        frame = frames[request.frame_index]
    else:
        # Use middle frame as default (often captures the key moment)
        frame = frames[len(frames) // 2]
    
    # Get context from video data
    context_parts = []
    if video_data.get("commentary_text"):
        context_parts.append(f"Commentary: {video_data['commentary_text'][:200]}")
    if video_data.get("funny_moment"):
        moment = video_data["funny_moment"]
        context_parts.append(f"Moment: {moment.get('description', '')}")
        context_parts.append(f"Why it's funny: {moment.get('reason', '')}")
    
    context = " | ".join(context_parts) if context_parts else ""
    
    try:
        # Generate meme
        meme_id = uuid.uuid4().hex[:12]
        output_path = str(settings.TEMP_DIR / f"meme_{meme_id}.png")
        
        result = await meme_engine.generate_meme(
            frame_base64=frame["image_base64"],
            context=context,
            output_path=output_path
        )
        
        # Upload to storage if available
        if storage_client.is_available():
            meme_url = await storage_client.upload_from_path(output_path)
        else:
            meme_url = f"file://{output_path}"
        
        # Store meme data for retrieval later (mirrors video_store pattern)
        meme_store[meme_id] = {
            "meme_id": meme_id,
            "meme_url": meme_url,
            "meme_path": output_path,
            "caption": result["caption"],
            "style": result["style"],
            "image_prompt": result["image_prompt"],
            "source_video_id": request.video_id,
            "source_frame_index": request.frame_index or len(frames) // 2,
            "source_frame_base64": frame["image_base64"],
            "context": context,
            "video_context": {
                "commentary_text": video_data.get("commentary_text", ""),
                "funny_moment": video_data.get("funny_moment", {}),
                "lens": str(video_data.get("lens", "")),
                "duration": video_data.get("video_info", {}).get("duration", 0),
            }
        }
        
        print(f"[Meme] ✅ Meme ready! Meme ID: {meme_id}")
        
        return MemeGenerateResponse(
            meme_id=meme_id,
            meme_url=meme_url,
            caption=result["caption"],
            style=result["style"],
            image_prompt=result["image_prompt"]
        )
        
    except Exception as e:
        print(f"[Meme] Error generating meme: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/meme/styles")
async def list_styles():
    """List available meme styles."""
    return {
        "styles": [
            {
                "id": "deepfried",
                "name": "Deep Fried",
                "description": "Oversaturated colors, lens flares, emojis, warped/distorted, ironic humor"
            },
            {
                "id": "surreal",
                "name": "Surreal",
                "description": "Weird edits, unexpected objects, dreamlike, absurd"
            },
            {
                "id": "wholesome",
                "name": "Wholesome",
                "description": "Clean edit with heartwarming twist, feel-good energy"
            },
            {
                "id": "cursed",
                "name": "Cursed",
                "description": "Unsettling, weird cropping, ominous energy"
            },
            {
                "id": "clean",
                "name": "Clean",
                "description": "Professional-looking meme, clear text overlays, polished"
            },
            {
                "id": "chaotic",
                "name": "Chaotic",
                "description": "Maximum chaos, multiple elements, sensory overload, gen-z brain rot"
            }
        ]
    }

@router.get("/api/meme/{meme_id}")
async def get_meme(meme_id: str):
    """Retrieve a generated meme by ID."""
    meme = meme_store.get(meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    return {
        "meme_id": meme.get("meme_id"),
        "meme_url": meme.get("meme_url"),
        "caption": meme.get("caption"),
        "style": meme.get("style"),
        "image_prompt": meme.get("image_prompt"),
        "source_video_id": meme.get("source_video_id"),
        "source_frame_index": meme.get("source_frame_index"),
        "context": meme.get("context"),
        "video_context": meme.get("video_context", {}),
    }


@router.get("/api/meme/templates")
async def list_templates():
    """List meme templates (legacy endpoint for compatibility)."""
    return {
        "templates": [
            {
                "id": "nano_banana",
                "name": "Nano Banana AI",
                "description": "AI-generated gen-z sports meme using Gemini's native image generation"
            }
        ]
    }


def get_meme_store() -> dict[str, dict]:
    """Get the in-memory meme store."""
    return meme_store