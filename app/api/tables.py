from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Table, Reservation
from app.db.database import get_db
from app.db.schemas.tables import TableGetResponse, TableResponse, TableCreate, TableDeleteResponse
from typing import List

router = APIRouter()

#В задание не было указано, что ендпоинты защищенные
#Решил не использовать асинхроную бд - так как делал это с MySQL
#сейчас ручка - синхронная но работает быстро, можно ускорить ее сделав запросы к бд асинхрооными
#решил добавить пагинацию - это хороший тон

@router.get("", response_model=List[TableGetResponse])
async def get_tables(
        #прмер с query GET /tables?skip=10&limit=5
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Table).offset(skip).limit(limit).all()


@router.post("", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(table_data: TableCreate, db: Session = Depends(get_db)):
    # Проверка — нет ли уже такого имени (необязательно)
    existing = db.query(Table).filter(Table.name == table_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table with name '{table_data.name}' already exists."
        )
    new_table = Table(**table_data.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


@router.delete("/{table_id}", response_model=TableDeleteResponse)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {table_id} not found."
        )

    db.delete(table)
    db.commit()
    return TableDeleteResponse(
        message="Table successfully deleted",
        deleted_id=table_id
    )
