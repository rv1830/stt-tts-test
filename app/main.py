from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import kundli, auth, chat, audio_test
from app.models.database import init_db
import os

app = FastAPI(title="ShubhRashi AI Platform")

# 1. Static Files Setup: Isse /static/ path browser mein khulega
static_path = "static"
if not os.path.exists(static_path):
    os.makedirs(static_path)

# Mount static folder taaki audio files access ho sakein
app.mount("/static", StaticFiles(directory=static_path), name="static")

# 2. Database Initialization
@app.on_event("startup")
def on_startup():
    init_db()

# 3. Routes/Endpoints
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(kundli.router, prefix="/api/kundli", tags=["Astrology"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])
app.include_router(audio_test.router, prefix="/api/audio", tags=["Audio Testing"])

@app.get("/")
def home():
    return {"message": "Astro-Dev Backend is Running"}