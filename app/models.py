import datetime
from typing import Optional
from pydantic import BaseModel, BaseSettings


class CSVFile(BaseModel):
    url: str


class SearchQuery(BaseModel):
    keyword: Optional[str]
    day: Optional[str]
    month: Optional[str]
    year: Optional[str]
    range_from: Optional[str]
    range_to: Optional[str]


class Settings(BaseSettings):
    password: str
    username: str
    host_url: str
    aws_access_key_id: str
    aws_secret_key: str

    class Config:
        env_file = "app/.env"

# settings = Settings()