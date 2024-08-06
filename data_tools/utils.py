import logging

import whisperx
from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL
import os
import cv2
import imagehash
from PIL import Image
import json
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "float32" if DEVICE == "cuda" else "int8"
BATCH_SIZE = 2 if DEVICE == "cuda" else 1

def save_transcription(transcription, audio_path):
    json_path = f"{audio_path}.json"
    with open(json_path, "w", encoding='utf8') as json_file:
        json.dump(transcription, json_file, indent=4)
    return json_path

def load_transcription(json_path):
    with open(json_path, "r", encoding='utf8') as json_file:
        transcription = json.load(json_file)
    return transcription

# data_tools/utils.py
def associate_screenshots_with_transcription(screenshots, transcription):
    trans_segments = transcription['segments']
    associated_data = []
    
    if not screenshots:
        return [(None, segment['text']) for segment in trans_segments]
    
    # Start with the first screenshot
    current_screenshot_path = screenshots[0][1]
    screenshot_index = 0
    
    for segment in trans_segments:
        # Check if there is a next screenshot and if the segment start time is after the next screenshot time
        if screenshot_index < len(screenshots) - 1 and segment['start'] > screenshots[screenshot_index + 1][0]:
            screenshot_index += 1
            current_screenshot_path = screenshots[screenshot_index][1]
        # Associate the current segment text with the current screenshot path
        if associated_data and associated_data[-1][0] == current_screenshot_path:
            # Append the current segment text to the last entry's text
            associated_data[-1] = (current_screenshot_path, associated_data[-1][1] + " " + segment['text'])
        else:
            associated_data.append((current_screenshot_path, segment['text']))
    
    return associated_data


def transcribe_audio(audio_path):
    model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(audio_path)
    transcription = model.transcribe(audio, batch_size=2, print_progress=True, combined_progress=True)
    return transcription


def process_frame(frame, frame_count, fps, prev_hash, hash_size, threshold, output_folder):
    timestamp = frame_count / fps
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    curr_hash = imagehash.average_hash(pil_image, hash_size=hash_size)
    if prev_hash is None or abs(curr_hash - prev_hash) > threshold:
        screenshot_path = os.path.join(output_folder, f"screenshot_{frame_count}.png")
        cv2.imwrite(screenshot_path, frame)
        return curr_hash, timestamp, screenshot_path
    return prev_hash, None, None

def extract_screenshots_generator(video_path, output_folder="./tmp/screenshots", hash_size=8, threshold=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    prev_hash = None
    
    success, frame = cap.read()
    while success:
        frame_count += 1
        prev_hash, timestamp, screenshot_path = process_frame(frame, frame_count, fps, prev_hash, hash_size, threshold, output_folder)
        if screenshot_path:
            yield timestamp, screenshot_path
        success, frame = cap.read()
    
    cap.release()

def extract_screenshots(video_path, output_folder="./tmp/screenshots", hash_size=8, threshold=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    prev_hash = None
    screenshots = []
    
    success, frame = cap.read()
    while success:
        frame_count += 1
        prev_hash, timestamp, screenshot_path = process_frame(frame, frame_count, fps, prev_hash, hash_size, threshold, output_folder)
        if screenshot_path:
            screenshots.append((timestamp, screenshot_path))
        success, frame = cap.read()
    
    cap.release()
    return screenshots


def download_video(video_input, video_download_path):
    # Check if the input is a full URL or just an ID
    if video_input.startswith("http"):
        url = video_input
    else:
        url = f"https://www.youtube.com/watch?v={video_input}"
    
    logging.info("Downloading %s", url)

    ydl_opts = {
        "outtmpl": f"{video_download_path}/%(title)s.%(ext)s",  # Save path template
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

        info_dict = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info_dict)

    return filename


def convert_videos_to_mp3(source_path, destination_path):
    '''
    It will load all videos files from source_path. Then converts to mp3 and save it to destination_path
    '''
    logging.info("Converting videos to mp3")

    # create destination folder if not exists
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    videos = [f for f in os.listdir(source_path) if f.endswith(".mp4") or f.endswith(".webm")]

    for video in videos:
        video_path = os.path.join(source_path, video)
        audio_path = os.path.join(destination_path, f"{os.path.splitext(video)[0]}.mp3")
        
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)


def convert_video_to_audio(video_path):
    audio_path = f"{video_path}.mp3"

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    return audio_path


def transcribe_mp3s(source_path: str, target_path: str):
    model = whisperx.load_model("large-v2", DEVICE, compute_type=COMPUTE_TYPE)

    audios = [f for f in os.listdir(source_path) if f.endswith(".mp3")]

    for audio in audios:
        result = model.transcribe(f"{source_path}/{audio}")

        result_path = os.path.join(target_path, f"{os.path.splitext(audio)[0]}.json")
        with open(result_path, "w", encoding='utf8') as json_file:
            json.dump(result, json_file, indent=4)


def diarize_speakers(audio_path: str):
    audio = whisperx.load_audio(audio_path)
    model = whisperx.load_model("large-v2", DEVICE, compute_type=COMPUTE_TYPE)

    transcription = model.transcribe(audio_path, batch_size=BATCH_SIZE, print_progress=True)

    align_model, metadata = whisperx.load_align_model(
        language_code=transcription["language"], device=DEVICE
    )

    aligned_transcription = whisperx.align(
        transcription["segments"],
        align_model,
        metadata,
        audio,
        device=DEVICE,
        return_char_alignments=False,
    )
    
    diarize_model = whisperx.DiarizationPipeline(device=DEVICE)

    diarization_result = diarize_model(audio)

    return whisperx.assign_word_speakers(diarization_result, aligned_transcription)


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