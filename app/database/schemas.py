from pydantic import BaseModel


class DayCreate(BaseModel):
    date: str


class Day(BaseModel):
    id: int
    date: str

    class Config:
        orm_mode = True
