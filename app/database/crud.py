from sqlalchemy.orm import Session

from . import models, schemas


def get_day(db: Session, day_id: int):
    return db.query(models.Day).filter(models.Day.id == day_id).first()


def get_day_by_date(db: Session, date: str):
    return db.query(models.Day).filter(models.Day.date == date).first()


def get_days(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Day).offset(skip).limit(limit).all()


def create_day(db: Session, day: schemas.DayCreate):
    db_day = models.Day(date=day.date)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day
