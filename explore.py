import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus

MUSIC_APP_HINTS = ["spotify"]
VIDEO_APP_HINTS = ["chrome", "msedge", "firefox", "brave", "vivaldi", "vlc", "mpv"]

def matches(aumid, hints):
    aumid_lower = aumid.lower()
    return any(hint in aumid_lower for hint in hints) # loops through every keyword in hints, checks for substring of aumid_lower, returns True if match

async def main():
    manager = await MediaManager.request_async() # asks windows for the current media session manager
    sessions = manager.get_sessions() # returns a list of whatever Windows thinks is a media session
    for s in sessions:
        info = s.get_playback_info()
        print(s.source_app_user_model_id, PlaybackStatus(info.playback_status).name) # prints the app name and the playback status of each session
        if matches(s.source_app_user_model_id, MUSIC_APP_HINTS):
            print(s.source_app_user_model_id, "-> classified as MUSIC")
        elif matches(s.source_app_user_model_id, VIDEO_APP_HINTS):
            print(s.source_app_user_model_id, "-> classified as VIDEO")

asyncio.run(main())