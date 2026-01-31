# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

ragebAIt is a CLI tool that posts images/videos with captions to X (Twitter) using browser-use with local Chrome automation. Media and descriptions are provided by the user — there is no AI caption generation.

## Commands

```bash
uv sync                                    # install dependencies
uv run main.py <filepath> "<caption>"      # post with CLI args
uv run main.py                             # interactive mode
```

## Architecture

Two-file design:

- **main.py** — Entry point. Parses CLI args or prompts interactively, validates the media file, runs a Y/E/S confirmation loop, then calls `poster.post_to_x()`.
- **poster.py** — Launches local Chrome using the user's existing profile (Default) via browser-use. A `ChatGoogle` agent (gemini-2.0-flash) navigates x.com, composes a post with the caption, attaches the local media file, and publishes.

The flow is linear: input → confirm → browser agent posts with local file → report result.

## Key Details

- Uses `uv` for dependency management (pyproject.toml, not requirements.txt).
- Local Chrome automation — no cloud browser needed. Chrome must be fully closed before running.
- Authentication is via the user's existing Chrome profile with saved cookies. The env var `GEMINI_API_KEY` is required for the LLM.
- Media files are referenced by absolute local path — no upload step needed since Chrome runs locally.
- Supported image formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`. Video formats (`.mp4`, `.mov`) are accepted by `main.py` and may work depending on X's web UI constraints.
- Python 3.14+.
