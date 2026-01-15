from fastapi import APIRouter, UploadFile, File, Form
from elevenlabs.client import ElevenLabs
from deepgram import DeepgramClient
import os
import shutil
import uuid

router = APIRouter()

# API Key initialization (Keyword argument used as per v5)
dg_client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
client_eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# --- 1. SPEECH TO TEXT (Deepgram v5+ Standard) ---
@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    temp_file_path = f"temp_{uuid.uuid4()}_{file.filename}"
    
    # Audio file ko temporary save karna
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        with open(temp_file_path, "rb") as audio_file:
            # DOCUMENTATION FIX: 
            # 1. 'request' parameter mein direct bytes jayenge (audio_file.read())
            # 2. 'model' aur baki options direct keyword arguments ki tarah jayenge
            response = dg_client.listen.v1.media.transcribe_file(
                request=audio_file.read(), # Direct bytes as per README
                model="nova-2",            # Astrology ke liye best model
                smart_format=True,
                language="hi"              # Hindi/Hinglish support
            )
            
            # Response parsing logic
            transcript = response.results.channels[0].alternatives[0].transcript
            return {"text": transcript}

    except Exception as e:
        return {"error": f"Deepgram Error: {str(e)}"}
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# --- 2. TEXT TO SPEECH (ElevenLabs) ---
@router.post("/tts")
async def text_to_speech(text: str = Form(...)):
    try:
        audio_generator = client_eleven.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM", 
            text=text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        audio_bytes = b"".join(list(audio_generator))
        
        file_name = f"test_{uuid.uuid4()}.mp3"
        file_path = f"static/{file_name}"
        os.makedirs("static", exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        
        return {"audio_url": f"http://localhost:8000/static/{file_name}"}
    except Exception as e:
        return {"error": f"ElevenLabs Error: {str(e)}"}