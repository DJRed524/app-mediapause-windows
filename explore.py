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
        aumid = s.source_app_user_model_id # shorthand for the giant WinRT session object
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
    prev_music_playing = None # state from last check, so we can spot changes
    prev_video_playing = None
    paused_music_by_us = False # true if the script paused it, not the user manually
    paused_video_by_us = False
    while True:
        music_session, video_sessions = await check_once()
        music_playing = is_playing(music_session)
        video_playing = any(is_playing(v) for v in video_sessions)
        print("music_playing:", music_playing, "| video_playing:", video_playing)

        # first loop, no previous state yet - just record baseline and skip
        if prev_music_playing is None:
            prev_music_playing = music_playing
            prev_video_playing = video_playing
            print("---")
            await asyncio.sleep(2)
            continue

        video_just_started = video_playing and not prev_video_playing # wasn't playing last check, is now
        music_just_started = music_playing and not prev_music_playing

        if video_just_started and music_playing:
            print("[auto] video started -> pausing music")
            await music_session.try_pause_async()
            paused_music_by_us = True # script paused it, so script is allowed to resume it later

        elif music_just_started and video_playing:
            print("[auto] music started -> pausing video")
            for v in video_sessions:
                await v.try_pause_async()
            paused_video_by_us = True # same idea, for video

        if paused_music_by_us and not video_playing:
            print("[auto] video stopped -> resuming music")
            await music_session.try_play_async()
            paused_music_by_us = False # no longer holding a pause

        if paused_video_by_us and not music_playing:
            print("[auto] music stopped -> resuming video")
            for v in video_sessions:
                await v.try_play_async()
            paused_video_by_us = False

        prev_music_playing = music_playing # save state for next loop
        prev_video_playing = video_playing

        print("---")
        await asyncio.sleep(2)

asyncio.run(main())