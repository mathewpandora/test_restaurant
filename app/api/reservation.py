from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Reservation, Table
from app.db.database import get_db
from datetime import timedelta
from app.db.schemas.reservations import ReservationBase, ReservationCreate, ReservationResponse
from sqlalchemy import text

router = APIRouter()

@router.get("", response_model=List[ReservationResponse])
def get_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Reservation).offset(skip).limit(limit).all()

# 🔹 Создать бронь
@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли стол
    table = db.query(Table).filter(Table.id == data.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail=f"Table {data.table_id} not found")

    start_time = data.reservation_time
    end_time = start_time + timedelta(minutes=data.duration_minutes)
    # Проверяем на пересечение с другими резервациями.
    # Используем выражение SQL: reservation_time + duration_minutes * interval '1 minute'
    overlapping = db.query(Reservation).filter(
        Reservation.table_id == data.table_id,
        Reservation.reservation_time < end_time,
        (Reservation.reservation_time + (Reservation.duration_minutes * text("interval '1 minute'"))) > start_time
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Time conflict with another reservation "
                f"(id={overlapping.id}, starts at {overlapping.reservation_time})"
            )
        )

    new_reservation = Reservation(**data.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# 🔹 Удалить бронь
@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail=f"Reservation {reservation_id} not found")

    db.delete(reservation)
    db.commit()
    return None