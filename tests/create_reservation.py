import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000/reservation"

async def create_reservation():
    payload = {
        "customer_name": "John Doe",
        "table_id": 5,  # Убедитесь, что стол с таким id существует
        "reservation_time": datetime(2025, 4, 10, 19, 0).isoformat(),  # Формат в ISO 8601
        "duration_minutes": 90
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=payload)
        print("POST status:", response.status_code)
        print("POST response:", response.json())

# Запуск асинхронной функции
async def main():
    await create_reservation()

if __name__ == "__main__":
    asyncio.run(main())
