from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from app.db.models import Table, Reservation
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

# Загрузка переменных окружения
load_dotenv()

# Подключение к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

# Модели Pydantic для ответов API
class TableResponse(BaseModel):
    id: int
    name: str
    seats: int
    location: Optional[str]

    class Config:
        orm_mode = True

class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/tables/", response_model=List[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@app.get("/reservations/", response_model=List[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()
