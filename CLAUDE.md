# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

ragebAIt is a CLI tool that posts images/videos with captions to X (Twitter) using Browser-Use Cloud browser automation. Media and descriptions are provided by the user — there is no AI caption generation.

## Commands

```bash
uv sync                                    # install dependencies
uv run main.py <filepath> "<caption>"      # post with CLI args
uv run main.py                             # interactive mode
```

## Architecture

Two-file design:

- **main.py** — Entry point. Parses CLI args or prompts interactively, validates the media file, runs a Y/E/S confirmation loop, then calls `poster.post_to_x()`.
- **poster.py** — Creates a Browser-Use Cloud session using a persistent `cloud_profile_id` (pre-authenticated, no credentials sent to the LLM). Instructs a `ChatBrowserUse()` agent to navigate x.com, compose a post, attach the media file, and publish.

The flow is linear: input → confirm → browser agent posts → report result.

## Key Details

- Uses `uv` for dependency management (pyproject.toml, not requirements.txt).
- Browser-Use Cloud handles all browser infra — no local Chrome needed.
- Authentication is via a cloud profile with saved cookies. The env vars are `BROWSER_USE_API_KEY` and `BROWSER_USE_PROFILE_ID`.
- Supported media formats: `.jpg`, `.png`, `.gif`, `.webp`, `.mp4`, `.mov`.
- Python 3.14+.
