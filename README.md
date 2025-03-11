# Voice-to-Text Transcription App

A Streamlit application that records audio from your microphone and transcribes it to text using Groq's Whisper model.

## Features

- Record audio directly from your microphone
- Adjust recording duration
- Transcribe speech to text using Whisper Large v3
- Simple and intuitive user interface

## Requirements

- Python 3.8+
- FFmpeg installed on your system
- Groq API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/voice-text-ai.git
cd voice-text-ai
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`

4. Make sure FFmpeg is installed and update the path in `audio_recorder.py` if necessary.

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `audio_recorder.py`: Audio recording functionality
- `transcription.py`: Speech-to-text transcription using Groq
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked by git)

## License

MIT 