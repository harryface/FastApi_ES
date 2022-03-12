import logging
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from typing import Optional

from .database import models
from .database.settings import engine

from .es_service import StartIndexing, search
from .models import SearchQuery

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


@app.get("/manual-index/")
def manually_index():
    indexing = StartIndexing()
    indexing.start()
    return {"message": "Initiated"}


@app.get("/run-cron/")
def run_cron():
    '''
    Receive iso date and runs the indexing for that day
    '''
    indexing = StartIndexing()
    indexing.start()
    return {"message": "Initiated"}


@app.post("/search/", status_code=200)
def search_item(search_query: SearchQuery):
    # csv_dict = csv_file.dict()
    # return csv_dict
    # return bulk_insert(csv_file.url)
    result = search(
        search_query.keyword,
        search_query.year,
        search_query.month,
        search_query.day,
        search_query.range_from,
        search_query.range_to,
    )
    return result


# @app.post("/index/", status_code=status.HTTP_201_CREATED)
# def index_item(csv_file: CSVFile):
#     # csv_dict = csv_file.dict()
#     # return csv_dict
#     return bulk_insert(csv_file.url)


# @app.get("/search/", status_code=200)
# def search_item(keyword: Optional[str] = None, year: Optional[str] = None, month: Optional[str] = None, day: Optional[str] = None):
#     return search(keyword , year , month , day)
