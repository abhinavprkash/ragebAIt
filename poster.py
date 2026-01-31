import os

from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv()


async def post_to_x(filepath: str, caption: str) -> bool:
    abs_path = os.path.abspath(filepath)

    browser = Browser(use_cloud=True)

    agent = Agent(
        task=(
            f"Go to x.com. Log in with username x_user and password x_pass. "
            f"Create a new post with this text: '{caption}'. "
            f"Upload the file at '{abs_path}' as media attachment. "
            f"Then click the Post button to publish it."
        ),
        llm=ChatBrowserUse(),
        browser=browser,
        sensitive_data={
            "x_user": os.getenv("X_USERNAME"),
            "x_pass": os.getenv("X_PASSWORD"),
        },
        use_vision=False,
        max_steps=25,
    )

    try:
        result = await agent.run()
        return result.is_done()
    except Exception as e:
        print(f"Browser agent error: {e}")
        return False
    finally:
        await browser.close()
