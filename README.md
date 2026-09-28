# app-mediapause-windows

Automatically pauses Spotify when a video starts playing, and pauses the video when Spotify starts so the two don't end up playing over each other. Whichever one it paused gets auto-resumed once the other stops. Anything you pause manually is left alone.

## Status

Core logic works. Still to do: wrap it in a tray icon with an on/off toggle so it can run quietly in the background instead of a terminal window.

## How it works

Uses Windows' built-in media session system (SMTC), the same thing behind your keyboard's play/pause button, through a Python package called winsdk. It polls every 2 seconds, tracks what changed since the last check, and only pauses/resumes things it paused itself.

## Installation

1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install winsdk`

## Requirements

- Windows 10/11
- Python 3.x