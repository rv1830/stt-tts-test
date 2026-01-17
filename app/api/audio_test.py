import os
import uuid
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form
from elevenlabs.client import ElevenLabs

router = APIRouter()

# ElevenLabs Client initialization
client_eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket Connected (Automated Voice Loop Mode)")
    
    try:
        while True:
            # 1. Browser se text receive karna
            data = await websocket.receive_json()
            user_text = data.get("text")
            
            if user_text:
                print(f"User said: {user_text}")

                # 2. Automated TTS Generation
                # Yahan hum wahi text ElevenLabs ko bhej rahe hain playback ke liye
                response_text = f"{user_text}"
                
                audio_generator = client_eleven.text_to_speech.convert(
                    voice_id="21m00Tcm4TlvDq8ikWAM", 
                    text=response_text,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                
                audio_bytes = b"".join(list(audio_generator))
                file_name = f"auto_{uuid.uuid4()}.mp3"
                file_path = f"static/{file_name}"
                os.makedirs("static", exist_ok=True)

                with open(file_path, "wb") as f:
                    f.write(audio_bytes)

                # 3. Frontend ko text aur Audio URL dono ek saath bhej dena
                await websocket.send_json({
                    "message": response_text,
                    "audio_url": f"http://localhost:3005/static/{file_name}",
                    "type": "voice_response"
                })

    except WebSocketDisconnect:
        print("User disconnected")
    except Exception as e:
        print(f"Voice Loop Error: {e}")

# Manual TTS Endpoint (Keeping it for debugging)
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
        file_name = f"manual_{uuid.uuid4()}.mp3"
        file_path = f"static/{file_name}"
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return {"audio_url": f"http://localhost:3005/static/{file_name}"}
    except Exception as e:
        return {"error": str(e)}