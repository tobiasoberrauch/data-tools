import streamlit as st
import cv2
import numpy as np
from PIL import Image
import imagehash
import os

def extract_screenshots(video_path, output_folder="screenshots", hash_size=8, threshold=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    
    prev_hash = None
    frame_count = 0
    screenshot_count = 0
    
    while success:
        frame_count += 1
        
        # Convert frame to PIL image for hashing
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        curr_hash = imagehash.average_hash(pil_image, hash_size=hash_size)
        
        # Compare the current frame hash to the previous frame hash
        if prev_hash is None or abs(curr_hash - prev_hash) > threshold:
            screenshot_path = os.path.join(output_folder, f"screenshot_{frame_count}.png")
            cv2.imwrite(screenshot_path, frame)
            screenshot_count += 1
            prev_hash = curr_hash
        
        success, frame = cap.read()
    
    cap.release()
    return screenshot_count, output_folder

# Streamlit UI
st.title("Video Screenshot Extractor")

uploaded_file = st.file_uploader("Upload an MP4 or MKV file", type=["mp4", "mkv"])

if uploaded_file is not None:
    video_path = os.path.join("temp", uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("Extracting screenshots...")
    screenshot_count, output_folder = extract_screenshots(video_path)
    st.write(f"Extracted {screenshot_count} screenshots.")
    
    if screenshot_count > 0:
        st.write("Screenshots:")
        for screenshot in os.listdir(output_folder):
            st.image(os.path.join(output_folder, screenshot), use_column_width=True)
