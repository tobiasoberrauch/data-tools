import json
import os
import sys
from contextlib import contextmanager

import psutil
from yt_dlp import YoutubeDL

from data_tools.utils import convert_video_to_audio, diarize_speakers


@contextmanager
def monitor_resources(section_name):
    # Measure resource usage before the code block
    cpu_start = psutil.cpu_percent(interval=None)
    ram_start = psutil.virtual_memory().percent
    disk_start = psutil.disk_usage("/").percent

    yield

    # Measure resource usage after the code block
    cpu_end = psutil.cpu_percent(interval=None)
    ram_end = psutil.virtual_memory().percent
    disk_end = psutil.disk_usage("/").percent

    print(f"--- {section_name} ---")
    print(f"CPU start: {cpu_start}% -> end: {cpu_end}%")
    print(f"RAM start: {ram_start}% -> end: {ram_end}%")
    print(f"Disk start: {disk_start}% -> end: {disk_end}%")


def process_video(video_info, parent_dir):
    with monitor_resources("Video Download and Processing"):
        downloaded_video_file = video_info["requested_downloads"][0]["filename"]
        video_id = video_info["id"]
        video_title = video_info["title"]

        video_dir = os.path.join(parent_dir, f"{video_id} = {video_title}")
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

        video_file = os.path.join(
            video_dir, f"video.{downloaded_video_file.split('.')[-1]}"
        )
        os.rename(downloaded_video_file, video_file)

        audio_file = os.path.join(video_dir, "audio.mp3")
        transcript_file = os.path.join(video_dir, "transcript.json")
        metadata_file = os.path.join(video_dir, "metadata.json")
        transcript_txt_file = os.path.join(video_dir, "transcript.txt")

        # Filter out non-serializable objects
        serializable_video_info = {
            key: value
            for key, value in video_info.items()
            if is_json_serializable(value)
        }

        with open(metadata_file, "w") as f:
            json.dump(serializable_video_info, f, indent=4)

        with monitor_resources("Audio Conversion"):
            convert_video_to_audio(video_file, audio_file)

        with monitor_resources("Transcription and Diarization"):
            transcription, _ = diarize_speakers(audio_file)
            with open(transcript_file, "w") as f:
                json.dump(transcription, f, indent=4)

        txt_output = [segment["text"] for segment in transcription["segments"]]
        with open(transcript_txt_file, "w") as f:
            f.write("\n".join(txt_output))


def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False


def process_search_results(ydl, search_results, parent_dir):
    for entry in search_results["entries"]:
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
        video_info = ydl.extract_info(video_url, download=True)
        process_video(video_info, parent_dir)


def main(mode, identifier):
    ydl_opts = {
        "outtmpl": "./data/%(id)s.%(ext)s",
    }

    with YoutubeDL(ydl_opts) as ydl:
        if mode == "search":
            parent_dir = os.path.join(
                "./data", f"search_{identifier.replace(' ', '_')}"
            )
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            search_results = ydl.extract_info(
                f"ytsearch10:{identifier}", download=False
            )
            process_search_results(ydl, search_results, parent_dir)
        elif mode == "playlist":
            parent_dir = os.path.join("./data", f"playlist_{identifier}")
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            ydl_opts["extract_flat"] = "in_playlist"
            playlist_info = ydl.extract_info(identifier, download=False)
            for entry in playlist_info["entries"]:
                video_info = ydl.extract_info(entry["url"], download=True)
                process_video(video_info, parent_dir)
        elif mode == "video":
            video_info = ydl.extract_info(identifier, download=True)
            process_video(video_info, "./data")
        else:
            print("Invalid mode. Please use 'search', 'playlist', or 'video'.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pipeline.py {mode} {identifier}")
        print("Modes: search {query}, playlist {id}, video {id}")
        sys.exit(1)

    mode = sys.argv[1]
    identifier = sys.argv[2]
    main(mode, identifier)
