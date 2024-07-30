import streamlit as st
import whisperx
import json
import os

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(audio_path)
    transcription = model.transcribe(audio, batch_size=2, print_progress=True, combined_progress=True)
    return transcription

def save_transcription(transcription, audio_path):
    json_path = f"{audio_path}.json"
    with open(json_path, "w") as json_file:
        json.dump(transcription, json_file, indent=4)
    return json_path

# Streamlit UI
st.title("Audio Transcription App")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file is not None:
    audio_path = os.path.join("temp", uploaded_file.name)
    
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
        st.download_button(label="Download Transcription", data=open(json_path).read(), file_name=f"{uploaded_file.name}.json", mime="application/json")

        # Display the transcription
        st.json(transcription)

