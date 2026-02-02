"""
ragebAIt - Share Router
Handles posting generated content to X (Twitter) via browser automation.
"""

import subprocess
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException

from backend.config import settings

router = APIRouter(tags=["share"])

# In-memory store for share job status
share_jobs: dict[str, dict] = {}

BROWSER_AUTO_DIR = settings.MEDIA_DIR.parent  # browser-auto/


def _run_post_cli(share_id: str) -> None:
    """Run browser-auto/post_cli.py in its own uv environment (blocking)."""
    import json

    share_jobs[share_id]["status"] = "posting"

    try:
        result = subprocess.run(
            ["uv", "run", "post_cli.py"],
            cwd=str(BROWSER_AUTO_DIR),
            capture_output=True,
            text=True,
            timeout=180,  # 3-minute timeout
        )

        # post_cli.py prints a single JSON line to stdout
        stdout = result.stdout.strip()
        if stdout:
            payload = json.loads(stdout.splitlines()[-1])
        else:
            payload = {"success": False, "error": result.stderr.strip() or "No output from post_cli"}

        if payload.get("success"):
            share_jobs[share_id]["status"] = "completed"
        else:
            share_jobs[share_id]["status"] = "failed"
            share_jobs[share_id]["error"] = payload.get("error", "Unknown error")

    except subprocess.TimeoutExpired:
        share_jobs[share_id]["status"] = "failed"
        share_jobs[share_id]["error"] = "Browser automation timed out (3 min)"
    except Exception as e:
        share_jobs[share_id]["status"] = "failed"
        share_jobs[share_id]["error"] = str(e)


@router.post("/api/share/x")
async def share_to_x(background_tasks: BackgroundTasks):
    """
    Start posting the current media (video + meme + caption) to X.

    Returns immediately with a share_id that can be polled for status.
    """
    media_dir = settings.MEDIA_DIR

    # Validate that the required media files exist
    required = {"video.mp4": media_dir / "video.mp4",
                "image.png": media_dir / "image.png",
                "caption.txt": media_dir / "caption.txt"}

    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing media files: {', '.join(missing)}")

    share_id = uuid.uuid4().hex[:12]
    share_jobs[share_id] = {"status": "pending", "error": None}

    background_tasks.add_task(_run_post_cli, share_id)

    return {"share_id": share_id, "status": "pending"}


@router.get("/api/share/{share_id}/status")
async def get_share_status(share_id: str):
    """
    Poll the status of a share job.

    Status values: pending | posting | completed | failed
    """
    job = share_jobs.get(share_id)
    if not job:
        raise HTTPException(status_code=404, detail="Share job not found")

    return {"share_id": share_id, "status": job["status"], "error": job.get("error")}
