import streamlit as st
from get_transcript import generate_transcript
from index import build_chain

st.title("YouTube Video Chatt")

# Input for YouTube URL
url = st.text_input("Enter the video URL")

# Generate transcript only once and store in session state
if url and "transcript" not in st.session_state:
    st.write("Downloading and transcribing video... this may take a while...")
    transcript = generate_transcript(url)
    if transcript:
        st.session_state.transcript = transcript
        st.session_state.final_chain = build_chain(transcript)
        st.success("Transcript generated!")

# Ask questions only if transcript exists
if "final_chain" in st.session_state:
    query = st.text_input("Ask a question about the Video")
    if query:
        try:
            result = st.session_state.final_chain.invoke(query)
            st.write("📋 Answer:", result)
        except Exception as e:
            st.error(f"Error: {e}")
