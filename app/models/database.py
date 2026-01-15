from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import uuid
from datetime import datetime

# Settings se URL uthayega jo .env mein hai
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone = Column(String, unique=True, nullable=False)
    name = Column(String)
    credits = Column(Integer, default=0)

class Kundli(Base):
    __tablename__ = "kundlis"
    kundli_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True) # Nullable for testing
    name = Column(String, nullable=False)
    chart_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)