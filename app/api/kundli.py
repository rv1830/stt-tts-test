from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.astrology import ProKeralaService
from app.models.database import SessionLocal, Kundli
import uuid

router = APIRouter()
astro_service = ProKeralaService()

# Database session manage karne ke liye helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_kundli(
    name: str, 
    dob: str, 
    tob: str, 
    lat: float, 
    lon: float, 
    db: Session = Depends(get_db)
):
    # ProKerala Format: YYYY-MM-DDTHH:MM:SSZ
    # SANDBOX NOTE: Only Jan 1st (01-01) is allowed!
    formatted_datetime = f"{dob}T{tob}:00+05:30"
    
    params = {
        "datetime": formatted_datetime,
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1
    }
    
    # 1. External API Call
    data = await astro_service.get_kundli_data(params)
    
    if data.get("status") == "error":
        return {"error": "ProKerala API Error", "details": data.get("errors")}
        
    # 2. Database mein Save karna
    try:
        new_kundli = Kundli(
            kundli_id=str(uuid.uuid4()),
            name=name,
            chart_data=data # Pura JSON save ho raha hai
        )
        db.add(new_kundli)
        db.commit()
        db.refresh(new_kundli)
        
        return {
            "status": "Success",
            "message": "Kundli created and saved to DB",
            "kundli_id": new_kundli.kundli_id,
            "data": data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")