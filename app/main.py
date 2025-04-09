from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from app.api import tables, reservation
import os

# Загрузка переменных окружения
load_dotenv()

# Подключение к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservation.router, prefix="/reservation", tags=["reservation"])

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
    return {"message": "Благодарю, что уделили время на проверку тестовго! Очень прошу вас дать мне обратную связь по коду, даже если ваше решение негативное",
            "contact":{"tg":"@waterspelling", "whatsapp":"89153029475"},
            "resume":"https://mathewresume.online"}




