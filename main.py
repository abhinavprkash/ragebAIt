import asyncio
import os
import sys

from poster import post_to_x

SUPPORTED_FORMATS = {".jpg", ".png", ".gif", ".webp", ".mp4", ".mov"}


def get_input():
    if len(sys.argv) >= 3:
        filepath = sys.argv[1]
        caption = sys.argv[2]
    else:
        filepath = input("Media file path: ").strip()
        caption = input("Caption: ").strip()

    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}")
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"Error: unsupported format '{ext}'. Supported: {', '.join(sorted(SUPPORTED_FORMATS))}")
        sys.exit(1)

    return filepath, caption


def confirm(filepath, caption):
    print(f"\nFile:    {filepath}")
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
    filepath, caption = get_input()
    caption = confirm(filepath, caption)
    if caption is None:
        print("Skipped.")
        return

    print("Posting...")
    success = await post_to_x(filepath, caption)
    if success:
        print("Posted successfully.")
    else:
        print("Failed to post.")


if __name__ == "__main__":
    asyncio.run(main())
