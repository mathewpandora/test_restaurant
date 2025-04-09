from pydantic import BaseModel
from typing import Optional

class TableGetResponse(BaseModel):
    id: int
    name: str
    seats: int
    location: Optional[str]

    class Config:
        orm_mode = True

class TableCreate(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None

class TableResponse(BaseModel):
    id: int
    name: str
    seats: int
    location: Optional[str] = None

    class Config:
        orm_mode = True

class TableDeleteResponse(BaseModel):
    message: str
    deleted_id: int