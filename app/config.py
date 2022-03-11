import requests
from functools import lru_cache
from .models import Settings


@lru_cache()
def get_settings():
    return Settings()


username = get_settings().username
password = get_settings().password
hostname = get_settings().host_url
index = "security"

session = requests.Session()
session.auth = (username, password)
