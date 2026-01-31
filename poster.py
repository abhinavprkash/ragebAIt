import os

from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv()


async def post_to_x(filepath: str, caption: str) -> bool:
    abs_path = os.path.abspath(filepath)

    browser = Browser(
        cloud_profile_id=os.getenv("BROWSER_USE_PROFILE_ID"),
    )

    agent = Agent(
        task=(
            f"Go to x.com. You are already logged in. "
            f"Create a new post with this text: '{caption}'. "
            f"Upload the file at '{abs_path}' as media attachment. "
            f"Then click the Post button to publish it."
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
