from sqlalchemy import Column, Integer, String

from .settings import Base


class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)
