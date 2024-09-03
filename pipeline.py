import json
import os
import sys
from yt_dlp import YoutubeDL
from data_tools.utils import convert_video_to_audio, diarize_speakers

def create_directory(directory_path):
    """Creates a directory if it does not already exist."""
    os.makedirs(directory_path, exist_ok=True)

def save_json(data, file_path):
    """Saves data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def save_text(data, file_path):
    """Saves text data to a file."""
    with open(file_path, "w") as f:
        f.write("\n".join(data))

def process_video(video_info, parent_dir, local_audio_file=None):
    if local_audio_file:
        audio_file = local_audio_file
        base_name = os.path.splitext(os.path.basename(local_audio_file))[0]
        video_dir = os.path.join(parent_dir, f"local_{base_name}")
        create_directory(video_dir)
    else:
        downloaded_video_file = video_info["requested_downloads"][0]["filename"]
        video_id = video_info["id"]
        video_title = video_info["title"]

        video_dir = os.path.join(parent_dir, f"{video_id} = {video_title}")
        create_directory(video_dir)

        video_file = os.path.join(video_dir, f"video.{downloaded_video_file.split('.')[-1]}")
        os.rename(downloaded_video_file, video_file)

        audio_file = os.path.join(video_dir, "audio.mp3")
        convert_video_to_audio(video_file, audio_file)

        # Save metadata only if processing a video
        metadata_file = os.path.join(video_dir, "metadata.json")
        serializable_video_info = {key: value for key, value in video_info.items() if is_json_serializable(value)}
        save_json(serializable_video_info, metadata_file)

    # Transcription and diarization
    transcript_file = os.path.join(video_dir, "transcript.json")
    transcript_txt_file = os.path.join(video_dir, "transcript.txt")

    transcription, _ = diarize_speakers(audio_file)
    save_json(transcription, transcript_file)

    txt_output = [segment["text"] for segment in transcription["segments"]]
    save_text(txt_output, transcript_txt_file)

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

    parent_dir_map = {
        "search": lambda id: os.path.join("./data", f"search_{id.replace(' ', '_')}"),
        "playlist": lambda id: os.path.join("./data", f"playlist_{id}"),
        "video": lambda _: "./data",
        "local": lambda _: "./data"
    }

    with YoutubeDL(ydl_opts) as ydl:
        if mode not in parent_dir_map:
            print("Invalid mode. Please use 'search', 'playlist', 'video', or 'local'.")
            sys.exit(1)

        parent_dir = parent_dir_map[mode](identifier)
        create_directory(parent_dir)

        if mode == "search":
            search_results = ydl.extract_info(f"ytsearch10:{identifier}", download=False)
            process_search_results(ydl, search_results, parent_dir)
        elif mode == "playlist":
            ydl_opts["extract_flat"] = "in_playlist"
            playlist_info = ydl.extract_info(identifier, download=False)
            for entry in playlist_info["entries"]:
                video_info = ydl.extract_info(entry["url"], download=True)
                process_video(video_info, parent_dir)
        elif mode == "video":
            video_info = ydl.extract_info(identifier, download=True)
            process_video(video_info, parent_dir)
        elif mode == "local":
            if not os.path.isfile(identifier):
                print(f"Local file {identifier} not found.")
                sys.exit(1)
            process_video(None, parent_dir, local_audio_file=identifier)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pipeline.py {mode} {identifier}")
        print("Modes: search {query}, playlist {id}, video {id}, local {path_to_m4a}")
        sys.exit(1)

    mode = sys.argv[1]
    identifier = sys.argv[2]
    main(mode, identifier)
