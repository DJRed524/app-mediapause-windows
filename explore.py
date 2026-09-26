import asyncio
import time
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus

MUSIC_APP_HINTS = ["spotify"]
VIDEO_APP_HINTS = ["chrome", "msedge", "firefox", "brave", "vivaldi", "vlc", "mpv"]

def matches(aumid, hints):
    aumid_lower = aumid.lower()
    return any(hint in aumid_lower for hint in hints) # loops through every keyword in hints, checks for substring of aumid_lower, returns True if match

async def check_once():
    manager = await MediaManager.request_async()
    sessions = manager.get_sessions()
    music_session = None
    video_sessions = []
    for s in sessions:
        aumid = s.source_app_user_model_id
        info = s.get_playback_info()
        print(aumid, PlaybackStatus(info.playback_status).name)
        if matches(aumid, MUSIC_APP_HINTS):
            music_session = s
        elif matches(aumid, VIDEO_APP_HINTS):
            video_sessions.append(s)
    return music_session, video_sessions

def is_playing(session):
    if session is None:
        return False
    return PlaybackStatus(session.get_playback_info().playback_status) == PlaybackStatus.PLAYING

async def main():
    while True:
        music_session, video_sessions = await check_once()
        music_playing = is_playing(music_session)
        video_playing = any(is_playing(v) for v in video_sessions)
        print("music_playing:", music_playing, "| video_playing:", video_playing)
        print("---")
        time.sleep(2)

asyncio.run(main())