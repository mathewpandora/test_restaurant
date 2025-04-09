import httpx
import asyncio

BASE_URL = "http://localhost:8000/tables"

"""
Ответ: 

POST status: 201
POST response: {'id': 6, 'name': 'Table 102', 'seats': 4, 'location': 'Terrace'}
GET status: 200
GET response: [{'id': 1, 'name': 'Table 1', 'seats': 4, 'location': 'Near window'}, {'id': 2, 'name': 'Table 2', 'seats': 6, 'location': 'Center'}, {'id': 3, 'name': 'Table 3', 'seats': 2, 'location': 'Bar area'}, {'id': 4, 'name': 'Table 4', 'seats': 8, 'location': 'Private room'}, {'id': 5, 'name': 'Table 101', 'seats': 4, 'location': 'Terrace'}, {'id': 6, 'name': 'Table 102', 'seats': 4, 'location': 'Terrace'}]
DELETE status: 200
DELETE response: {'message': 'Table successfully deleted', 'deleted_id': 6}
GET status: 200
GET response: [{'id': 1, 'name': 'Table 1', 'seats': 4, 'location': 'Near window'}, {'id': 2, 'name': 'Table 2', 'seats': 6, 'location': 'Center'}, {'id': 3, 'name': 'Table 3', 'seats': 2, 'location': 'Bar area'}, {'id': 4, 'name': 'Table 4', 'seats': 8, 'location': 'Private room'}, {'id': 5, 'name': 'Table 101', 'seats': 4, 'location': 'Terrace'}]
"""
async def create_table():
    payload = {
        "name": "Table 102",
        "seats": 4,
        "location": "Terrace"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=payload)
        print("POST status:", response.status_code)
        print("POST response:", response.json())
        return response.json().get("id")


async def get_tables(skip=0, limit=5):
    params = {"skip": skip, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        print("GET status:", response.status_code)
        print("GET response:", response.json())


async def delete_table(table_id: int):
    url = f"{BASE_URL}/{table_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        print("DELETE status:", response.status_code)
        try:
            print("DELETE response:", response.json())
        except Exception:
            print("DELETE response: <no content>")


async def main():
    # Создаём столик
    table_id = await create_table()

    # Проверим, что он появился
    await get_tables(skip=0, limit=10)

    # Удалим его
    if table_id:
        await delete_table(table_id)

    # Проверим, что удалился
    await get_tables(skip=0, limit=10)


if __name__ == "__main__":
    asyncio.run(main())
