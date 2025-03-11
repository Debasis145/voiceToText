import os
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transcriber:
    def __init__(self, api_key=None, model="whisper-large-v3"):
        """
        Initialize the Transcriber with Groq API key and model.
        
        Args:
            api_key (str): Groq API key. If None, it will be loaded from environment variables.
            model (str): The model to use for transcription.
        """
        # Get API key from environment variables if not provided
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            logging.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
            raise ValueError("Groq API key not found")
        
        self.model = model
        self.client = Groq(api_key=self.api_key)
    
    def transcribe(self, audio_file_path, language="en"):
        """
        Transcribe audio file to text.
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe.
            language (str): Language code for transcription.
            
        Returns:
            str: Transcribed text.
        """
        try:
            logging.info(f"Transcribing audio file: {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language
                )
            
            logging.info("Transcription complete.")
            return transcription.text
            
        except Exception as e:
            logging.error(f"An error occurred during transcription: {e}")
            return f"Error during transcription: {str(e)}" 