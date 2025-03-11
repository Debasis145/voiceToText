import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioRecorder:
    def __init__(self, ffmpeg_path="C:/ffmpeg/bin/ffmpeg.exe"):
        """
        Initialize the AudioRecorder with the path to FFmpeg.
        
        Args:
            ffmpeg_path (str): Path to the FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path
        # Add FFmpeg to the PATH
        os.environ["PATH"] += os.pathsep + os.path.dirname(self.ffmpeg_path)
        # Set FFmpeg binary path for pydub
        AudioSegment.converter = self.ffmpeg_path
        self.recognizer = sr.Recognizer()
        
    def record_audio(self, file_path=None, timeout=5, phrase_time_limit=None):
        """
        Record audio from the microphone and save it as an MP3 file.
        
        Args:
            file_path (str): Path to save the recorded audio file. If None, a temporary file is created.
            timeout (int): Maximum time to wait for a phrase to start (in seconds).
            phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
            
        Returns:
            str: Path to the saved audio file
        """
        # If no file path is provided, create a temporary file
        if file_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            file_path = temp_file.name
            temp_file.close()
        
        try:
            with sr.Microphone() as source:
                logging.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Start speaking now...")
                
                # Record the audio
                audio_data = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete.")
                
                # Convert the recorded audio to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
                audio_segment.export(file_path, format="mp3", bitrate="128k")
                
                logging.info(f"Audio saved to {file_path}")
                return file_path

        except sr.WaitTimeoutError:
            logging.warning("No speech detected within the timeout period.")
            return None
        except Exception as e:
            logging.error(f"An error occurred during recording: {e}")
            return None 