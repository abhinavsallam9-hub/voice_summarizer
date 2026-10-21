"""Web interface: upload audio -> get transcript + summary."""
import os
import tempfile

import streamlit as st

from summarizer import summarize
from transcriber import transcribe

st.set_page_config(page_title="AI Audio Summarizer", page_icon="🎙️")
st.title("🎙️ AI Audio-to-Text Summarizer")
st.write("Upload a lecture, meeting or study-session recording. "
         "Whisper converts speech to text, then Generative AI writes the summary.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API key (optional)", type="password",
                            value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Free key: aistudio.google.com/apikey. Without a key, a basic offline summary is used.")

audio = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "ogg", "flac", "webm"])

if audio is not None:
    st.audio(audio)
    if st.button("Transcribe & Summarize", type="primary"):
        suffix = os.path.splitext(audio.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio.getbuffer())
            path = tmp.name

        with st.spinner("Step 1/2: Converting speech to text with Whisper..."):
            transcript, lang = transcribe(path)
        os.remove(path)

        with st.spinner("Step 2/2: Summarizing..."):
            summary, method = summarize(transcript, api_key.strip() or None)

        st.subheader("📝 Summary")
        st.caption(f"Method: {method}")
        st.markdown(summary)

        st.subheader("📄 Full Transcript")
        st.caption(f"Detected language: {lang}")
        st.text_area("Transcript", transcript, height=250, label_visibility="collapsed")

        st.download_button("Download transcript + summary",
                           f"SUMMARY\n\n{summary}\n\nTRANSCRIPT\n\n{transcript}",
                           file_name="summary.txt")
