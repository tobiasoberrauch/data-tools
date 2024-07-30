import streamlit as st

from data_tools.utils import download_video, transcribe_video

# Initialize your Streamlit app
st.title("YouTube Video Downloader and Transcriber")

video_url = st.text_input("Enter YouTube video URL")
download_path = st.text_input("Enter download path", "./tmp")

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
