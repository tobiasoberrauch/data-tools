import streamlit as st
from data_tools.utils import download_video, transcribe_video, download_playlist

# Initialize your Streamlit app
st.title("YouTube Video Downloader and Transcriber")

# Input for video URL
video_url = st.text_input("Enter YouTube video URL")
download_path = st.text_input("Enter download path", "./efrag/bronze")

if st.button("Download and Transcribe"):
    video_path = download_video(video_url, download_path)
    if video_path:
        st.write("Video downloaded to:", video_path)
        transcription = transcribe_video(video_path)
        if transcription:
            st.write("Transcription:")
            st.write(transcription)
        else:
            st.error("Transcription failed.")
    else:
        st.error("Video download failed.")

# Input for playlist ID
playlist_id = st.text_input("Enter YouTube playlist ID")

if st.button("Download Playlist"):
    success = download_playlist(playlist_id, download_path)
    if success:
        st.write("Playlist downloaded successfully.")
    else:
        st.error("Playlist download failed.")