import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def main():
    manager = await MediaManager.request_async() # asks windows for the current media session manager
    sessions = manager.get_sessions() # returns a list of whatever Windows thinks is a media session
    for s in sessions:
        print(s.source_app_user_model_id) # the app's identifier string

asyncio.run(main())