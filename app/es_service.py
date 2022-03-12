import json
from contextlib import contextmanager
from typing import Optional
from datetime import datetime

from fastapi import HTTPException
import pandas as pd

from .database import crud, schemas
from .database.settings import SessionLocal
from .aws_boto import create_presigned_url

from .config import index, hostname, session, todays_date
from .worker import index_data


# yield db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def search(
    keyword: Optional[str] = None,
    year: Optional[str] = None,
    month: Optional[str] = None,
    day: Optional[str] = None,
    range_from: Optional[str] = None,
    range_to: Optional[str] = None,
):
    """
    Feed in date and keyword, for a search
    """

    search_data = {"query": {"bool": {"should": []}}}

    if keyword:
        search_data["query"]["bool"]["should"].append({"match": {"summary": keyword}})
        search_data["query"]["bool"]["should"].append({"match": {"topic": keyword}})
        search_data["query"]["bool"]["should"].append({"match": {"headline": keyword}})
    if year:
        search_data["query"]["bool"]["should"].append({"match": {"year": year}})
    if month:
        search_data["query"]["bool"]["should"].append({"match": {"month": month}})
    if day:
        search_data["query"]["bool"]["should"].append({"match": {"day": day}})
    if range_from and range_to:
        search_data["query"]["bool"]["filter"] = {"range": {"date": {"gte": range_from, "lte": range_to}}}

    if len(search_data["query"]["bool"]["should"]) == 0:
        search_data = {"query": {"match_all": {}}}
        # So we will not give out all data
        return {}
    print(search_data)

    try:
        response = session.post(
            url=f"{hostname}{index}/_search/", json=search_data
        ).text
        result = json.loads(response)
    except Exception as e:
        raise HTTPException(
            status_code=503, detail="The elasticsearch is not reachable"
        )

    return result.get("hits", {}).get("hits", {})


class StartIndexing:
    """
    For the scheduler
    Get a presigned url for the day, get its data
    and add rows to celery.
    NB: we need to check if it has been called before.
    """

    def __init__(self):
        pass

    def start(self):
        # get date
        date = todays_date
        # check if date exists
        with contextmanager(get_db)() as db:
            db_day = crud.get_day_by_date(db, date=date)
            # if it does, do nothing else, run index
            if db_day:
                return
            else:
                url = create_presigned_url()
                if url:
                    answer = self.__bulk_insert(url)
                    if answer:
                        crud.create_day(db=db, day=schemas.DayCreate(date=date))
        return

    def __bulk_insert(self, url):
        """
        Receives the url, reads it into a dataframe, then
        send the df to a function that would push the data
        line by line to celery.
        """
        # https://medium.com/analytics-vidhya/optimized-ways-to-read-large-csvs-in-python-ab2b36a7914e
        # https://towardsdatascience.com/apply-function-to-pandas-dataframe-rows-76df74165ee4
        # Read in the csv
        try:
            df = pd.read_csv(url)
            # push to worker
            answer = self.__push_to_worker(df)
        except Exception as e:
            print("error", e)
            raise HTTPException(
                status_code=503, detail="The csv url served is not working"
            )

        return answer

    def __push_to_worker(self, df):
        """
        Pushes the rows of the dataframe to celery workers
        nb: datetime could be an issue
        """

        for x in zip(
            df["Year"],
            df["Month"],
            df["Day"],
            df["ActionGeo_FullName"],
            df["Source_Url"],
            df["Summary"],
            df["topic"],
            df["Headline"],
        ):
            body = {
                "year": x[0],
                "month": x[1],
                "day": x[2],
                "date": f"{x[0]}-{str(x[1]).zfill(2)}-{str(x[2]).zfill(2)}",
                "action_geo_full_name": x[3],
                "source_url": x[4],
                "summary": x[5],
                "topic": x[6],
                "headline": x[7],
            }
            # Send to celery worker
            index_data.delay(body)

        return True



