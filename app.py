# app.py
# uses streamlit for the ui

import streamlit as st
from notetaker import get_transcript, transcript_notes
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="YouTube NoteTaker", layout="centered")

st.title("🎥🤓 YouTube Video Note Taker")

video_url = st.text_input("Enter YouTube video URL")

if st.button("Notes"):
    if not video_url:
        st.error("Please enter a valid YouTube URL.")
    else:
        try:
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_url)
            with st.spinner("Taking Notes..."):
                notes = transcript_notes(transcript)
            st.subheader("📝 Notes:")
            st.write(notes)
        except Exception as e:
            st.error(f"Error: {e}")
