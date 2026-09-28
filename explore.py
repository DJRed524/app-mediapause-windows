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
        print(aumid, PlaybackStatus(info.playback_status).name) # prints the app name and the playback status of each session
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
    prev_music_playing = None  # state from the last check, so we can detect changes
    prev_video_playing = None
    paused_music_by_us = False  # tracks whether WE paused it (vs. the user pausing it manually)
    paused_video_by_us = False
    while True:
        music_session, video_sessions = await check_once()
        music_playing = is_playing(music_session)
        video_playing = any(is_playing(v) for v in video_sessions)
        print("music_playing:", music_playing, "| video_playing:", video_playing)

        # first loop ever - no "previous" state to compare against yet, so just
        # record the baseline and skip straight to the next check
        if prev_music_playing is None:
            prev_music_playing = music_playing
            prev_video_playing = video_playing
            print("---")
            await asyncio.sleep(2)
            continue

        # "just started" = wasn't playing last check, IS playing now
        video_just_started = video_playing and not prev_video_playing
        music_just_started = music_playing and not prev_music_playing

        # video started while music's playing -> pause music
        if video_just_started and music_playing:
            print("[auto] video started -> pausing music")
            await music_session.try_pause_async()
            paused_music_by_us = True  # remember it was us, so we know to resume it later

        # music started while video's playing -> pause the video(s)
        elif music_just_started and video_playing:
            print("[auto] music started -> pausing video")
            for v in video_sessions:
                await v.try_pause_async()
            paused_video_by_us = True

        # video has stopped, and WE were the one who paused music -> resume music
        if paused_music_by_us and not video_playing:
            print("[auto] video stopped -> resuming music")
            await music_session.try_play_async()
            paused_music_by_us = False  # reset - we're no longer "holding" a pause

        # music has stopped, and WE were the one who paused video -> resume video
        if paused_video_by_us and not music_playing:
            print("[auto] music stopped -> resuming video")
            for v in video_sessions:
                await v.try_play_async()
            paused_video_by_us = False

        # save current state as "last check" for the next loop iteration
        prev_music_playing = music_playing
        prev_video_playing = video_playing

        print("---")
        await asyncio.sleep(2)

asyncio.run(main())