import streamlit as st
from moviepy.editor import VideoFileClip


def convert_to_mp3(video_path):
    audio_path = f"{video_path}.mp3"
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path


st.title("MP4 to MP3 Converter")

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
