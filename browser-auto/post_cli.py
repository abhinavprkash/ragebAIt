"""
Non-interactive CLI wrapper around poster.post_to_x().
Reads media/video.mp4, media/image.png, and media/caption.txt,
validates they exist, posts to X, and prints a JSON result to stdout.

Invoked by the backend as:
    uv run post_cli.py
"""

import asyncio
import json
import os
import sys

from poster import post_to_x

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")

IMAGE_PATH = os.path.join(MEDIA_DIR, "image.png")
VIDEO_PATH = os.path.join(MEDIA_DIR, "video.mp4")
CAPTION_PATH = os.path.join(MEDIA_DIR, "caption.txt")


def result_json(success: bool, error: str = "") -> str:
    return json.dumps({"success": success, "error": error})


async def main() -> None:
    # Validate required files
    missing = []
    for label, path in [("image", IMAGE_PATH), ("video", VIDEO_PATH), ("caption", CAPTION_PATH)]:
        if not os.path.isfile(path):
            missing.append(f"{label} ({path})")

    if missing:
        print(result_json(False, f"Missing files: {', '.join(missing)}"))
        sys.exit(1)

    caption = open(CAPTION_PATH).read().strip()
    if not caption:
        print(result_json(False, "caption.txt is empty"))
        sys.exit(1)

    try:
        success = await post_to_x(IMAGE_PATH, VIDEO_PATH, caption)
        print(result_json(success, "" if success else "Browser agent reported failure"))
    except Exception as e:
        print(result_json(False, str(e)))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
