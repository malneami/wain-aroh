"""
Text-to-Speech Service
Converts AI text responses to natural Arabic speech using Piper TTS
"""

import subprocess
import io
import os
import tempfile
from pydub import AudioSegment

class TextToSpeechService:
    """
    Converts text responses to speech using Piper TTS for natural-sounding Arabic voices
    """
    
    def __init__(self):
        # Path to Piper model
        self.model_path = "/home/ubuntu/wain_aroh_backend/models/piper/ar_JO-kareem-medium.onnx"
        self.piper_command = "piper"
        
        # Check if model exists
        if not os.path.exists(self.model_path):
            print(f"Warning: Piper model not found at {self.model_path}")
            print("Falling back to gTTS")
            self.use_piper = False
        else:
            self.use_piper = True
            print(f"Piper TTS initialized with model: {self.model_path}")
        
    def text_to_speech(self, text, voice=None, speed=1.0):
        """
        Convert text to speech using Piper TTS
        
        Args:
            text: Text to convert (Arabic or English)
            voice: Voice to use (not used for Piper)
            speed: Speech speed (0.5 to 2.0, default 1.0)
            
        Returns:
            Audio data as bytes (MP3 format)
        """
        if self.use_piper:
            try:
                return self._piper_tts(text, speed)
            except Exception as e:
                print(f"Error in Piper TTS: {e}")
                print("Falling back to gTTS...")
                return self._gtts_fallback(text)
        else:
            return self._gtts_fallback(text)
    
    def _piper_tts(self, text, speed=1.0):
        """Generate speech using Piper TTS"""
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_file:
            wav_path = wav_file.name
        
        try:
            # Adjust length scale (inverse of speed)
            # speed 1.0 = length_scale 1.0 (normal)
            # speed 2.0 = length_scale 0.5 (faster)
            # speed 0.5 = length_scale 2.0 (slower)
            length_scale = 1.0 / speed if speed > 0 else 1.0
            length_scale = max(0.5, min(2.0, length_scale))  # Clamp to reasonable range
            
            # Run Piper command
            cmd = [
                self.piper_command,
                '-m', self.model_path,
                '-f', wav_path,
                '--length-scale', str(length_scale)
            ]
            
            # Pass text via stdin
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                raise Exception(f"Piper failed: {stderr}")
            
            # Convert WAV to MP3 using pydub
            audio = AudioSegment.from_wav(wav_path)
            
            # Export to MP3 in memory
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format='mp3', bitrate='128k')
            mp3_buffer.seek(0)
            
            return mp3_buffer.read()
            
        finally:
            # Clean up temporary file
            if os.path.exists(wav_path):
                os.unlink(wav_path)
    
    def _gtts_fallback(self, text):
        """Fallback to gTTS if Piper fails"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="ar", slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.read()
        except Exception as e:
            print(f"gTTS fallback also failed: {e}")
            return None
    
    def save_audio(self, audio_data, filepath):
        """Save audio data to file"""
        try:
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def get_available_voices(self):
        """Get list of available voices"""
        if self.use_piper:
            return {
                "kareem": "Kareem - Natural Arabic male voice (Piper TTS)"
            }
        else:
            return {
                "ar": "Arabic (Google TTS - Fallback)"
            }

# Global instance
tts_service = TextToSpeechService()

