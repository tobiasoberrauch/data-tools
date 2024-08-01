import os

import streamlit as st

from data_tools.utils import (
    associate_screenshots_with_transcription,
    convert_to_mp3,
    download_playlist,
    download_video,
    extract_screenshots,
    transcribe_video,
    save_transcription,
    transcribe_audio,
)

# Streamlit UI
st.title("Comprehensive YouTube and Audio Processing App")

# Automation section
st.header("Automate All Tasks")
video_input_auto = st.text_input("Enter YouTube video URL or ID for automation")
download_path_auto = st.text_input("Enter download path for automation", "./tmp")

if st.button("Automate All"):
    video_path_auto = download_video(video_input_auto, download_path_auto)
    if video_path_auto:
        st.write("Video downloaded to:", video_path_auto)

        st.write("Converting video to MP3...")
        audio_path_auto = convert_to_mp3(video_path_auto)

        st.write("Transcribing audio...")
        transcription_auto = transcribe_audio(audio_path_auto)
        json_path_auto = save_transcription(transcription_auto, audio_path_auto)

        st.write("Extracting screenshots...")
        screenshots_auto = extract_screenshots(video_path_auto, transcription_auto)

        st.write("Associating screenshots with transcription...")
        associated_data_auto = associate_screenshots_with_transcription(
            screenshots_auto, transcription_auto
        )

        st.success("All tasks completed successfully!")
        st.download_button(
            label="Download MP3",
            data=open(audio_path_auto, "rb"),
            file_name=f"{os.path.basename(audio_path_auto)}.mp3",
        )
        st.download_button(
            label="Download Transcription",
            data=open(json_path_auto).read(),
            file_name=f"{os.path.basename(audio_path_auto)}.json",
            mime="application/json",
        )

        st.write("Transcription and Screenshots:")
        for screenshot, text in associated_data_auto:
            st.image(screenshot, caption=text, use_column_width=True)
    else:
        st.error("Video download failed.")

# Section for YouTube video download and transcription
st.header("YouTube Video Downloader and Transcriber")
video_input = st.text_input("Enter YouTube video URL or ID")
download_path = st.text_input("Enter download path", "./tmp")

if st.button("Download and Transcribe Video"):
    video_path = download_video(video_input, download_path)
    if video_path:
        st.write("Video downloaded to:", video_path)
        transcription = transcribe_video(video_path)
        if transcription:
            st.write("Transcription:")
            st.write(transcription)

            st.write("Extracting screenshots...")
            screenshots = extract_screenshots(video_path, transcription)

            st.write("Associating screenshots with transcription...")
            associated_data = associate_screenshots_with_transcription(
                screenshots, transcription
            )

            st.write("Transcription and Screenshots:")
            for screenshot, text in associated_data:
                st.image(screenshot, caption=text, use_column_width=True)
        else:
            st.error("Transcription failed.")
    else:
        st.error("Video download failed.")

# Section for playlist download
st.header("YouTube Playlist Downloader")
playlist_id = st.text_input("Enter YouTube playlist ID")

if st.button("Download Playlist"):
    success = download_playlist(playlist_id, download_path)
    if success:
        st.write("Playlist downloaded successfully.")
    else:
        st.error("Playlist download failed.")

# Section for MP4 to MP3 conversion
st.header("MP4 to MP3 Converter")
uploaded_file_video = st.file_uploader("Upload an MP4 file", type=["mp4"])

if uploaded_file_video is not None:
    video_path = os.path.join("temp", uploaded_file_video.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file_video.getbuffer())

    st.write("Converting...")
    audio_path = convert_to_mp3(video_path)
    st.write("Conversion complete!")

    with open(audio_path, "rb") as f:
        st.download_button("Download MP3", f, file_name=audio_path)

# Section for audio transcription
st.header("Audio Transcription App")
uploaded_file_audio = st.file_uploader(
    "Upload an audio file", type=["mp3", "wav", "m4a", "mp4"], key="audio_uploader"
)

if uploaded_file_audio is not None:
    audio_path = os.path.join("temp", uploaded_file_audio.name)

    # Save uploaded file to disk
    with open(audio_path, "wb") as f:
        f.write(uploaded_file_audio.getbuffer())

    st.audio(audio_path, format="audio/mp3")

    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(audio_path)
            json_path = save_transcription(transcription, audio_path)

        st.success("Transcription complete!")
        st.download_button(
            label="Download Transcription",
            data=open(json_path).read(),
            file_name=f"{uploaded_file_audio.name}.json",
            mime="application/json",
        )

        st.json(transcription)
