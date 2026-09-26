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
    manager = await MediaManager.request_async() # asks windows for the current media session manager
    sessions = manager.get_sessions() # returns a list of whatever Windows thinks is a media session
    for s in sessions:
        aumid = s.source_app_user_model_id # shorthand for the giant WinRT session object
        info = s.get_playback_info()
        print(aumid, PlaybackStatus(info.playback_status).name) # prints the app name and the playback status of each session
        if matches(aumid, MUSIC_APP_HINTS):
            print(aumid, "-> classified as MUSIC")
        elif matches(aumid, VIDEO_APP_HINTS):
            print(aumid, "-> classified as VIDEO")

async def main():
    while True:
        await check_once()
        print("---")
        time.sleep(2)

asyncio.run(main())