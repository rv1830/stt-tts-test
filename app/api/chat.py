from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Kundli
from app.services.ai_engine import AIEngine

router = APIRouter()
ai_service = AIEngine()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/ask")
async def ask_question(kundli_id: str, question: str, db: Session = Depends(get_db)):
    # 1. Database se saved Kundli data nikalo
    kundli = db.query(Kundli).filter(Kundli.kundli_id == kundli_id).first()
    if not kundli:
        return {"error": "Kundli not found"}
    
    # 2. AI Engine ko data aur question bhejo
    prediction = await ai_service.generate_astrology_prediction(kundli.chart_data, question)
    
    return {
        "question": question,
        "prediction": prediction
    }