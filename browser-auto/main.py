import asyncio
import os
import sys
import httpx
from typing import Optional

from poster import post_to_x

IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_FORMATS = {".mp4", ".mov"}
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")

# Backend API base URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


async def fetch_from_backend(video_id: str, meme_id: str) -> Optional[dict]:
    """Fetch video URL, meme URL, and caption from the backend API."""
    async with httpx.AsyncClient() as client:
        try:
            # Fetch video data
            video_resp = await client.get(f"{BACKEND_URL}/api/video/{video_id}")
            video_resp.raise_for_status()
            video_data = video_resp.json()

            # Fetch meme data
            meme_resp = await client.get(f"{BACKEND_URL}/api/meme/{meme_id}")
            meme_resp.raise_for_status()
            meme_data = meme_resp.json()

            return {
                "video_url": video_data.get("video_url"),
                "meme_url": meme_data.get("meme_url"),
                "caption": meme_data.get("caption"),
                "style": meme_data.get("style"),
                "image_prompt": meme_data.get("image_prompt"),
            }
        except httpx.HTTPError as e:
            print(f"Error fetching from backend: {e}")
            return None


async def download_media(url: str, output_path: str) -> bool:
    """Download media from URL to local file."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, follow_redirects=True)
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(resp.content)
            return True
        except httpx.HTTPError as e:
            print(f"Error downloading {url}: {e}")
            return False


def list_media_by_type(extensions):
    """Return sorted list of media files matching the given extensions."""
    if not os.path.isdir(MEDIA_DIR):
        return []
    return sorted(
        f for f in os.listdir(MEDIA_DIR)
        if os.path.splitext(f)[1].lower() in extensions
    )


def pick_file(label, extensions):
    """Show numbered list of files matching extensions and let the user choose one."""
    files = list_media_by_type(extensions)
    if not files:
        print(f"Error: no {label} files found in {MEDIA_DIR}")
        sys.exit(1)

    print(f"\n{label} files:")
    for i, name in enumerate(files, 1):
        print(f"  {i}. {name}")

    while True:
        choice = input(f"Pick a {label.lower()} file (1-{len(files)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return os.path.join(MEDIA_DIR, files[int(choice) - 1])
        print("Invalid choice.")


def resolve_path(filename):
    """Resolve a filename to an absolute path, checking MEDIA_DIR if relative."""
    return os.path.join(MEDIA_DIR, filename) if not os.path.isabs(filename) else filename


def validate_file(filepath, label, extensions):
    """Validate that the file exists and has a supported extension."""
    if not os.path.isfile(filepath):
        print(f"Error: {label.lower()} file not found: {filepath}")
        sys.exit(1)
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in extensions:
        print(f"Error: unsupported {label.lower()} format '{ext}'. Supported: {', '.join(sorted(extensions))}")
        sys.exit(1)


def get_input():
    if len(sys.argv) >= 4:
        image_path = resolve_path(sys.argv[1])
        video_path = resolve_path(sys.argv[2])
        caption = sys.argv[3]
    else:
        image_path = pick_file("Image", IMAGE_FORMATS)
        video_path = pick_file("Video", VIDEO_FORMATS)
        caption = input("Caption: ").strip()

    validate_file(image_path, "Image", IMAGE_FORMATS)
    validate_file(video_path, "Video", VIDEO_FORMATS)

    return image_path, video_path, caption


def confirm(image_path, video_path, caption):
    print(f"\nImage:   {image_path}")
    print(f"Video:   {video_path}")
    print(f"Caption: {caption}\n")

    while True:
        choice = input("[Y]es / [E]dit / [S]kip: ").strip().lower()
        if choice in ("y", "yes"):
            return caption
        elif choice in ("e", "edit"):
            caption = input("New caption: ").strip()
            print(f"Caption: {caption}")
        elif choice in ("s", "skip"):
            return None
        else:
            print("Invalid choice.")


async def main():
    # Check if using backend API mode
    if len(sys.argv) >= 3 and sys.argv[1] == "--from-api":
        # Usage: python main.py --from-api <video_id> <meme_id>
        video_id = sys.argv[2]
        meme_id = sys.argv[3] if len(sys.argv) > 3 else None

        if not meme_id:
            print("Usage: python main.py --from-api <video_id> <meme_id>")
            sys.exit(1)

        print(f"Fetching from backend API (video: {video_id}, meme: {meme_id})...")
        data = await fetch_from_backend(video_id, meme_id)

        if not data:
            print("Failed to fetch data from backend.")
            sys.exit(1)

        # Download media files locally
        os.makedirs(MEDIA_DIR, exist_ok=True)
        video_path = os.path.join(MEDIA_DIR, f"{video_id}_video.mp4")
        image_path = os.path.join(MEDIA_DIR, f"{meme_id}_meme.png")

        print(f"Downloading video from {data['video_url']}...")
        if not await download_media(data["video_url"], video_path):
            sys.exit(1)

        print(f"Downloading meme from {data['meme_url']}...")
        if not await download_media(data["meme_url"], image_path):
            sys.exit(1)

        caption = data["caption"]
        print(f"\nFetched from API:")
        print(f"  Video: {video_path}")
        print(f"  Meme:  {image_path}")
        print(f"  Caption: {caption}")
        print(f"  Style: {data.get('style', 'unknown')}")
    else:
        # Original local file mode
        image_path, video_path, caption = get_input()

    caption = confirm(image_path, video_path, caption)
    if caption is None:
        print("Skipped.")
        return

    print("Posting...")
    success = await post_to_x(image_path, video_path, caption)
    if success:
        print("Posted successfully.")
    else:
        print("Failed to post.")


if __name__ == "__main__":
    asyncio.run(main())
