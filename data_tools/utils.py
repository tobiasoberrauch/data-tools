import logging

import whisperx
from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL


def download_video(video_id, video_download_path):
    url = f"https://www.youtube.com/watch?v={video_id}"
    logging.info("Downloading %s", url)

    ydl_opts = {
        "format": "best",  # Download the best available quality
        "outtmpl": f"{video_download_path}/%(title)s.%(ext)s",  # Save path template
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

        info_dict = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info_dict)

    return filename


def convert_to_mp3(video_path):
    audio_path = f"{video_path}.mp3"
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def convert_video_to_audio(video_path):
    audio_path = f"{video_path}.mp3"

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    return audio_path


def transcribe_video(video_path):
    try:
        # Load video
        audio_path = convert_video_to_audio(video_path)

        # Load whisper model
        DEVICE = "cpu"  # or 'cuda' if using GPU
        COMPUTE_TYPE = "float32"  # Change compute type to supported one
        model = whisperx.load_model("large-v2", DEVICE, compute_type=COMPUTE_TYPE)

        # Transcribe audio
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return None


def download_playlist(playlist_id, video_download_path):
    ydl_opts = {
        "outtmpl": f"{video_download_path}/%(id)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "yes_playlist": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/playlist?list={playlist_id}"])


def search_videos(query):
    ydl_opts = {
        #"quiet": True,
       # "simulate": True,
        #"extract_flat": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(f"ytsearch10:{query}", download=True)
