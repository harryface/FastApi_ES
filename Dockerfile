FROM nickgryg/alpine-pandas

# https://fastapi.tiangolo.com/deployment/docker/#behind-a-tls-termination-proxy
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]