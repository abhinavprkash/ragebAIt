"""
ragebAIt - Storage Client
Handles file uploads to Vercel Blob storage.
"""

import httpx
import shutil
import uuid
from pathlib import Path
from typing import Optional

from backend.config import settings


class StorageClient:
    """Client for Vercel Blob storage."""
    
    def __init__(self):
        self.token = settings.VERCEL_BLOB_TOKEN
        self.base_url = "https://blob.vercel-storage.com"
    
    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload a file to Vercel Blob.
        
        Args:
            file_bytes: File content as bytes
            filename: Desired filename
            content_type: MIME type of the file
            
        Returns:
            Public URL of the uploaded file
        """
        if not self.token:
            if settings.MOCK_MODE:
                # Return mock URL in mock mode
                return f"https://mock-storage.local/{filename}"
            raise RuntimeError("VERCEL_BLOB_TOKEN not configured")
        
        # Generate unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/{unique_filename}",
                content=file_bytes,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": content_type,
                    "x-content-type": content_type,
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Upload failed: {response.status_code} - {response.text}")
            
            result = response.json()
            return result.get("url", "")
    
    async def upload_video(self, file_bytes: bytes, filename: str) -> str:
        """Upload a video file."""
        content_type = "video/mp4"
        if filename.endswith(".mov"):
            content_type = "video/quicktime"
        elif filename.endswith(".webm"):
            content_type = "video/webm"
        
        return await self.upload_file(file_bytes, filename, content_type)
    
    async def upload_audio(self, file_bytes: bytes, filename: str) -> str:
        """Upload an audio file."""
        content_type = "audio/mpeg"
        if filename.endswith(".wav"):
            content_type = "audio/wav"
        
        return await self.upload_file(file_bytes, filename, content_type)
    
    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        """Upload an image file."""
        content_type = "image/jpeg"
        if filename.endswith(".png"):
            content_type = "image/png"
        elif filename.endswith(".gif"):
            content_type = "image/gif"
        elif filename.endswith(".webp"):
            content_type = "image/webp"
        
        return await self.upload_file(file_bytes, filename, content_type)
    
    async def upload_from_path(self, file_path: str) -> str:
        """
        Upload a file from disk.
        
        Args:
            file_path: Path to file on disk
            
        Returns:
            Public URL of the uploaded file
        """
        path = Path(file_path)
        
        with open(path, 'rb') as f:
            file_bytes = f.read()
        
        # Determine content type from extension
        ext = path.suffix.lower()
        content_types = {
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.webm': 'video/webm',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        
        content_type = content_types.get(ext, 'application/octet-stream')
        
        return await self.upload_file(file_bytes, path.name, content_type)
    
    def is_available(self) -> bool:
        """Check if storage is configured."""
        return bool(self.token) or settings.MOCK_MODE

    def clear_media(self):
        """Clear all files in the browser-auto/media/ directory."""
        media_dir = settings.MEDIA_DIR
        if media_dir.exists():
            for item in media_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        print(f"[Storage] Cleared media dir {media_dir}")

    def save_to_media(self, file_path: str, media_filename: str, caption: str = ""):
        """
        Save a file to browser-auto/media/.

        Args:
            file_path: Source file path on disk
            media_filename: Target filename (e.g. "video.mp4", "image.png")
            caption: Caption text to write to caption.txt
        """
        media_dir = settings.MEDIA_DIR
        media_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, media_dir / media_filename)

        (media_dir / "caption.txt").write_text(caption)

        print(f"[Storage] Saved {media_filename} + caption.txt to {media_dir}")


# Singleton instance
storage_client = StorageClient()
