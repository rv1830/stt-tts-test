from elevenlabs import save
from elevenlabs.client import ElevenLabs
import os
import uuid

class AudioEngine:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def text_to_speech(self, text: str):
        # Audio generate karna
        audio = self.client.generate(
            text=text,
            voice="Rachel", # Aap 'Adam' ya koi aur voice bhi choose kar sakte ho
            model="eleven_multilingual_v2" # Hindi aur English dono ke liye best hai
        )
        
        # Audio file ko temporary save karna
        file_name = f"prediction_{uuid.uuid4()}.mp3"
        file_path = f"static/{file_name}"
        
        # Ensure static folder exists
        os.makedirs("static", exist_ok=True)
        
        save(audio, file_path)
        return file_path