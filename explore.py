import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus

async def main():
    manager = await MediaManager.request_async() # asks windows for the current media session manager
    sessions = manager.get_sessions() # returns a list of whatever Windows thinks is a media session
    for s in sessions:
        info = s.get_playback_info()
        print(s.source_app_user_model_id, PlaybackStatus(info.playback_status).name) # prints the app name and the playback status of each session
        if "spotify" in s.source_app_user_model_id.lower():
            print("Pausing Spotify...")
            await s.try_pause_async()        

asyncio.run(main())