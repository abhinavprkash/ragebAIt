import os

import httpx
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv()

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


async def _upload_to_cloud_session(filepath: str, session_id: str, api_key: str) -> str:
    """Upload a local file to the cloud browser session via presigned URL.

    Returns the cloud-accessible fileName from the API response.
    """
    ext = os.path.splitext(filepath)[1].lower()
    content_type = MIME_TYPES.get(ext)
    if not content_type:
        raise ValueError(f"Unsupported file type for cloud upload: {ext}")

    size_bytes = os.path.getsize(filepath)
    file_name = os.path.basename(filepath)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Get presigned URL
        resp = await client.post(
            f"https://api.browser-use.com/api/v2/files/browsers/{session_id}/presigned-url",
            headers={
                "X-Browser-Use-API-Key": api_key,
                "Content-Type": "application/json",
            },
            json={
                "fileName": file_name,
                "contentType": content_type,
                "sizeBytes": size_bytes,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        # 2. Upload file to presigned URL using multipart form POST
        fields = data["fields"]
        with open(filepath, "rb") as f:
            upload_resp = await client.post(
                data["url"],
                data=fields,
                files={"file": (file_name, f, content_type)},
            )
            upload_resp.raise_for_status()

    return data["fileName"]


async def post_to_x(filepath: str, caption: str) -> bool:
    abs_path = os.path.abspath(filepath)

    browser = Browser(
        cloud_profile_id=os.getenv("BROWSER_USE_PROFILE_ID"),
        cloud_proxy_country_code="us",
    )

    try:
        await browser.start()

        session_id = browser._cloud_browser_client.current_session_id
        api_key = os.getenv("BROWSER_USE_API_KEY")
        cloud_filename = await _upload_to_cloud_session(abs_path, session_id, api_key)

        agent = Agent(
            task=(
                f"Go to x.com. You are already logged in. "
                f"First, click the post button to open the compose dialog. "
                f"Then type this text: '{caption}'. "
                f"Then upload the file named '{cloud_filename}' as a media attachment. "
                f"Finally, click the Post button to publish it."
            ),
            llm=ChatBrowserUse(),
            browser=browser,
            max_steps=25,
        )

        result = await agent.run()
        return result.is_done()
    except Exception as e:
        print(f"Browser agent error: {e}")
        return False
    finally:
        await browser.kill()
