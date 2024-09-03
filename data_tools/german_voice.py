import tempfile
from typing import Optional

import streamlit as st
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

st.title("Thorsten-Voice - einfach ausprobieren")
st.markdown(
    "* 🇩🇪 Eine qualititativ hochwertige, deutsche, künstliche Stimme, die offline erzeugt werden kann, sollte jedem Projekt kostenlos und ohne lizenzrechtliche Einschränkungen zur Verfügung stehen."
)
st.markdown(
    "* 🇺🇸 A high-quality German artificial voice that can be generated offline should be available to any project free of charge and without any licensing restrictions."
)
st.markdown(
    "* Ein ⭐ ist gerne gesehen: https://github.com/thorstenMueller/Thorsten-Voice"
)
st.markdown("* **Danke für's Abonnieren 😊: https://www.youtube.com/@ThorstenMueller**")
st.markdown("* Die Webseite des Projektes lautet: https://www.Thorsten-Voice.de")

text = st.text_area("Zu sprechender Text")
model = st.radio(
    "Welches Thorsten-Voice Modell möchtest Du testen?",
    ("Thorsten-VITS", "Thorsten-DDC"),
)

if text:
    # Load Thorsten-Voice TTS/Vocoder models
    # Thanks to Coqui for inspiration and code snipplets :)
    manager = ModelManager()

    if model == "Thorsten-VITS":
        model_path, config_path, model_item = manager.download_model(
            "tts_models/de/thorsten/vits"
        )
        code = """pip install tts==0.8.0
tts-server --model_name tts_models/de/thorsten/vits
http://localhost:5002 im Browser öffnen"""

    if model == "Thorsten-DDC":
        model_path, config_path, model_item = manager.download_model(
            "tts_models/de/thorsten/tacotron2-DDC"
        )
        code = """pip install tts==0.8.0
tts-server --model_name tts_models/de/thorsten/tacotron2-DDC
http://localhost:5002 im Browser öffnen"""

    vocoder_name: Optional[str] = model_item["default_vocoder"]
    vocoder_path = None
    vocoder_config_path = None
    if vocoder_name is not None:
        vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    synthesizer = Synthesizer(
        model_path,
        config_path,
        None,
        None,
        vocoder_path,
        vocoder_config_path,
    )

    wav = synthesizer.tts(text)
    filename = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    synthesizer.save_wav(wav, filename)

    audio_file = open(filename.name, "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/wav")

    st.header("Wie gefällt Dir meine freie Stimme?")
    st.markdown(
        "Lass es mich gerne wissen - https://twitter.com/ThorstenVoice - Danke."
    )

    st.header("Thorsten-Voice lokal ausführen:")
    st.code(code, language="shell")

