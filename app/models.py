import datetime
from typing import Optional
from pydantic import BaseModel, BaseSettings, ValidationError, validator


class CSVFileDate(BaseModel):
    date: str

    @validator("date")
    def date_must_be_iso(cls, v):
        try:
            datetime.datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Incorrect data format, should be YYYY-MM-DD")
        return v


class SearchQuery(BaseModel):
    keyword: Optional[str]
    location: Optional[str]
    day: Optional[str]
    month: Optional[str]
    year: Optional[str]
    range_from: Optional[str]
    range_to: Optional[str]

    @validator("range_from", "range_to")
    def date_must_be_iso(cls, v):
        try:
            datetime.datetime.strptime(v.range_from, "%Y-%m-%d")
            datetime.datetime.strptime(v.range_to, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Incorrect data format, should be YYYY-MM-DD")

        return v


class Settings(BaseSettings):
    password: str
    username: str
    host_url: str
    aws_access_key_id: str
    aws_secret_key: str

    class Config:
        env_file = "app/.env"
