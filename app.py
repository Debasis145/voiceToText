import streamlit as st
import os
import time
import logging
from audio_recorder import AudioRecorder
from transcription import Transcriber
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set page configuration
st.set_page_config(
    page_title="Voice-to-Text Transcription",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4B8BF5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5F6368;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stButton > button {
        background-color: #4B8BF5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #3C78D8;
    }
    .recording-indicator {
        color: red;
        font-weight: bold;
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker {
        50% {
            opacity: 0;
        }
    }
    .result-area {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #DADCE0;
        margin-top: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #5F6368;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">Voice-to-Text Transcription</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Record your voice and convert it to text using AI</p>', unsafe_allow_html=True)
    
    # Initialize session state variables if they don't exist
    if 'transcription' not in st.session_state:
        st.session_state.transcription = ""
    if 'audio_file_path' not in st.session_state:
        st.session_state.audio_file_path = None
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        ffmpeg_path="C:/ffmpeg/bin/ffmpeg.exe"
        # FFmpeg path setting
        #ffmpeg_path = st.text_input(
            #"FFmpeg Path", 
            #value="C:/ffmpeg/bin/ffmpeg.exe",
           # help="Path to the FFmpeg executable on your system"
        #)
        
        # Recording settings
        st.subheader("Recording Settings")
        timeout = st.slider(
            "Timeout (seconds)", 
            min_value=1, 
            max_value=60, 
            value=20,
            help="Maximum time to wait for speech to start"
        )
        
        phrase_time_limit = st.slider(
            "Maximum Recording Duration (seconds)", 
            min_value=1, 
            max_value=60000, 
            value=55000,
            help="Maximum duration of the recording"
        )
        
        # Transcription settings
        st.subheader("Transcription Settings")
        model = st.selectbox(
            "Model", 
            options=["whisper-large-v3"],
            help="Model to use for transcription"
        )
        
        language = st.selectbox(
            "Language", 
            options=["en", "bn", "es", "fr", "de", "it", "pt", "nl", "ru", "zh", "ja", "ko"],
            help="Language of the audio for transcription"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This app uses Groq's Whisper model to transcribe speech to text. "
            "Make sure your voice is clear and your pronunciation is good."
            "Select the language you want for translation."
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Record Audio")
        
        # Record button
        if st.button("🎙️ Start Recording"):
            with st.spinner("Recording..."):
                st.session_state.is_recording = True
                
                # Create a placeholder for the recording indicator
                recording_indicator = st.empty()
                recording_indicator.markdown('<p class="recording-indicator">● Recording...</p>', unsafe_allow_html=True)
                
                # Initialize the audio recorder
                recorder = AudioRecorder(ffmpeg_path=ffmpeg_path)
                
                # Record audio
                audio_file_path = recorder.record_audio(
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                # Update session state
                st.session_state.audio_file_path = audio_file_path
                st.session_state.is_recording = False
                
                # Clear the recording indicator
                recording_indicator.empty()
                
                if audio_file_path:
                    st.success("Recording completed successfully!")
                    
                    # Display audio player
                    st.audio(audio_file_path)
                else:
                    st.error("Recording failed. Please try again.")
    
    with col2:
        st.subheader("Transcribe Audio")
        
        # Transcribe button
        if st.button("✨ Transcribe"):
            if st.session_state.audio_file_path:
                with st.spinner("Transcribing..."):
                    # Initialize the transcriber
                    transcriber = Transcriber(model=model)
                    
                    # Transcribe the audio
                    transcription = transcriber.transcribe(
                        st.session_state.audio_file_path,
                        language=language
                    )
                    
                    # Update session state
                    st.session_state.transcription = transcription
                    
                    st.success("Transcription completed!")
            else:
                st.warning("Please record audio first.")
    
    # Display transcription result
    st.markdown("### Transcription Result")
    result_container = st.container()
    with result_container:
        st.markdown('<div class="result-area">', unsafe_allow_html=True)
        if st.session_state.transcription:
            st.write(st.session_state.transcription)
        else:
            st.write("No transcription available. Record and transcribe audio to see results here.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Copy to clipboard button
    if st.session_state.transcription:
        if st.button("📋 Copy to Clipboard"):
            st.write("Text copied to clipboard!")
            st.code(st.session_state.transcription)
    
    # Footer
    st.markdown('<div class="footer">Developed with ❤️ using Streamlit and Groq @DEBASIS-2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 