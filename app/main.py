import logging
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from typing import Optional

from .database import models
from .database.settings import engine

from .es_service import StartIndexing, search
from .models import CSVFileDate, SearchQuery

# Instantiate Database
models.Base.metadata.create_all(bind=engine)


# Instantiate FastAPI
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# for running the cron
def run_cron():
    indexing = StartIndexing()
    indexing.start()
    return


# Start the cron job
@app.on_event("startup")
def start_cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_cron, 'cron', minute='*/2')
    scheduler.start()


# Api for feed and search
@app.get("/")
def home():
    return {"message": "Welcome Home"}


@app.post("/manually-index/")
def manually_index(csv_file_date: CSVFileDate):
    # csv_file_date = csv_file_date.dict()
    resp = {
        "status": "Successfull",
        "message": "CSV data has been added to the queue"
    }
    indexing = StartIndexing()
    indexed = indexing.manual_start(csv_file_date.date)
    if indexed:
        return resp
    return {"status": "Error", "message": "Something went wrong", "detail": "Either it has been indexed, or the file is not available yet"}


@app.post("/search/", status_code=200)
def search_item(search_query: SearchQuery):
    # csv_dict = csv_file.dict()
    # return csv_dict
    # return bulk_insert(csv_file.url)
    result = search(
        search_query.lookup,
        search_query.keyword,
        search_query.location,
        search_query.year,
        search_query.month,
        search_query.day,
        search_query.range_from,
        search_query.range_to,
    )
    return result


# @app.get("/search/", status_code=200)
# def search_item(keyword: Optional[str] = None, year: Optional[str] = None, month: Optional[str] = None, day: Optional[str] = None):
#     return search(keyword , year , month , day)
