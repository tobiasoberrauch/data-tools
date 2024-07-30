import json

import streamlit as st
import whisperx
from moviepy.editor import VideoFileClip

from data_tools.utils import download_video


# Function to convert MP4 to MP3
def convert_to_mp3(video_path):
    audio_path = f"{video_path}.mp3"
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path


# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(audio_path)
    transcription = model.transcribe(
        audio, batch_size=2, print_progress=True, combined_progress=True
    )
    return transcription


def save_transcription(transcription, audio_path):
    json_path = f"{audio_path}.json"
    with open(json_path, "w") as json_file:
        json.dump(transcription, json_file, indent=4)
    return json_path


# Streamlit app
st.title("Multifunctional Media App")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose the app mode",
    ["YouTube Downloader", "MP4 to MP3 Converter", "Audio Transcription"],
)

if app_mode == "YouTube Downloader":
    st.header("YouTube Video Downloader")
    video_id = st.text_input("Enter YouTube video ID")
    download_path = "./tmp"

    if st.button("Download and Transcribe"):
        video_path = download_video(video_id, download_path)
        if video_path:
            st.write("Video downloaded to:", video_path)

elif app_mode == "MP4 to MP3 Converter":
    st.header("MP4 to MP3 Converter")
    uploaded_file = st.file_uploader("Upload an MP4 file", type=["mp4"])

    if uploaded_file is not None:
        video_path = uploaded_file.name
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("Converting...")
        audio_path = convert_to_mp3(video_path)
        st.write("Conversion complete!")

        with open(audio_path, "rb") as f:
            st.download_button("Download MP3", f, file_name=audio_path)

elif app_mode == "Audio Transcription":
    st.header("Audio Transcription App")
    uploaded_file = st.file_uploader(
        "Upload an audio file", type=["mp3", "wav", "m4a", "mp4"]
    )

    if uploaded_file is not None:
        audio_path = uploaded_file.name

        # Save uploaded file to disk
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.audio(audio_path, format="audio/mp3")

        # Transcribe button
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcription = transcribe_audio(audio_path)
                json_path = save_transcription(transcription, audio_path)

            st.success("Transcription complete!")
            st.download_button(
                label="Download Transcription",
                data=open(json_path).read(),
                file_name=f"{uploaded_file.name}.json",
                mime="application/json",
            )

            # Display the transcription
            st.json(transcription)
