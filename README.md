# app-mediapause-windows

Automatically pauses Spotify when a video starts playing, and pauses the
video when Spotify starts so the two don't end up playing over each
other. Whichever one it paused gets auto-resumed once the other stops.

## Status

Still in progress. So far it can detect what's currently playing and pause
individual apps; now I just need to wire together the actual pause/resume logic
and a tray icon toggle.

## How it works

Uses Windows' built-in media session system (SMTC), the same thing behind
your keyboard's play/pause button through `winsdk`.

## Installation

1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install winsdk`

## Requirements

- Windows 10/11
- Python 3.x
