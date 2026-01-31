import os

from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv()


async def post_to_x(filepath: str, caption: str) -> bool:
    abs_path = os.path.abspath(filepath)

    proxy_country = os.getenv("BROWSER_USE_PROXY_COUNTRY", "us")

    browser = Browser(
        cloud_profile_id=os.getenv("BROWSER_USE_PROFILE_ID"),
        cloud_proxy_country_code="us",
    )

    agent = Agent(
        task=(
            f"Go to x.com. You are already logged in. "
            f"First, click the post button to open the compose dialog. "
            f"Then type this text: '{caption}'. "
            f"Then upload the file at '{abs_path}' as a media attachment. "
            f"Finally, click the Post button to publish it."
        ),
        llm=ChatBrowserUse(),
        browser=browser,
        max_steps=25,
    )

    try:
        result = await agent.run()
        return result.is_done()
    except Exception as e:
        print(f"Browser agent error: {e}")
        return False
    finally:
        await browser.kill()
