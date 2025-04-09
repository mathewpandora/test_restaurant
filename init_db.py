import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Table, Reservation  # Импортируем модели из вашего приложения
from datetime import datetime, timedelta

# Подключение к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Проверяем, есть ли уже данные в таблицах
        if not db.query(Table).first():
            # Создаем тестовые столы
            tables = [
                Table(name="Table 1", seats=4, location="Near window"),
                Table(name="Table 2", seats=6, location="Center"),
                Table(name="Table 3", seats=2, location="Bar area"),
                Table(name="Table 4", seats=8, location="Private room"),
            ]
            db.add_all(tables)
            db.commit()

            # Создаем тестовые бронирования
            now = datetime.now()
            reservations = [
                Reservation(
                    customer_name="John Doe",
                    table_id=1,
                    reservation_time=now + timedelta(hours=1),
                    duration_minutes=90
                ),
                Reservation(
                    customer_name="Jane Smith",
                    table_id=2,
                    reservation_time=now + timedelta(hours=3),
                    duration_minutes=120
                ),
                Reservation(
                    customer_name="Bob Johnson",
                    table_id=3,
                    reservation_time=now + timedelta(days=1),
                    duration_minutes=60
                ),
            ]
            db.add_all(reservations)
            db.commit()

            print("Database initialized with test data")
        else:
            print("Database already contains data, skipping initialization")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()