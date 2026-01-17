import os
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions

router = APIRouter()

# Deepgram Client Initialization
# Note: Aapka API Key yahan environment se uthayega
DEEPGRAM_API_KEY = "8148731eaadc76078ff50abaab0d4d1c0727cc98"
client = DeepgramClient(DEEPGRAM_API_KEY)

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Deepgram WebSocket Connected")
    
    try:
        while True:
            # 1. Frontend se text receive karna (STT browser se aa raha hai ya direct text)
            data = await websocket.receive_json()
            user_text = data.get("text")
            
            if user_text:
                print(f"User said: {user_text}")
                
                # Humne filhal simple echo rakha hai, aap yahan Gemini ka logic daal sakte hain
                response_text = f"Deepgram sun raha hai: {user_text}"

                # 2. Deepgram TTS (Aura Model) Generation
                file_name = f"dg_{uuid.uuid4()}.mp3"
                file_path = f"static/{file_name}"
                os.makedirs("static", exist_ok=True)

                options = SpeakOptions(
                    model="aura-asteria-en", # Asteria ek female voice hai, kafi natural hai
                    encoding="mp3",
                    container="none"
                )

                # API Call to Deepgram for TTS
                response = client.speak.v1.save(file_path, {"text": response_text}, options)

                # 3. Frontend ko response aur Audio URL bhej dena
                await websocket.send_json({
                    "message": response_text,
                    "audio_url": f"http://localhost:3005/static/{file_name}",
                    "type": "voice_response"
                })

    except WebSocketDisconnect:
        print("Deepgram Session Disconnected")
    except Exception as e:
        print(f"Deepgram Error: {e}")