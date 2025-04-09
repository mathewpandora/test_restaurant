import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000/reservation"

async def create_reservation():
    # Форматируем reservation_time в ISO формат
    payload = {
        "customer_name": "John Doe",
        "table_id": 1,  # Убедись, что стол с таким id существует
        "reservation_time": "2025-04-10T19:00:00",
                            "duration_minutes": 90
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=payload)
        print("POST status:", response.status_code)
        print("POST response:", response.json())
        return response.json().get("id")


async def get_reservations(skip=0, limit=10):
    params = {"skip": skip, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        print("GET status:", response.status_code)
        print("GET response:", response.json())


async def delete_reservation(reservation_id: int):
    url = f"{BASE_URL}/{reservation_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        print("DELETE status:", response.status_code)
        try:
            print("DELETE response:", response.json())
        except Exception:
            print("DELETE response: <no content>")


async def main():
    # Создаём бронь
    reservation_id = await create_reservation()

    # Проверим, что она появилась
    await get_reservations()

    # Удалим бронь
    if reservation_id:
        await delete_reservation(reservation_id)

    # Проверим, что удалена
    await get_reservations()


if __name__ == "__main__":
    asyncio.run(main())
