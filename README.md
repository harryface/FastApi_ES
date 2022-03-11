# Spinning Up On Local System
- Download  and install docker from www.docker.com
- CD into the root folder of the application
- On your terminal, run `docker-compose build`
- On your terminal, run `docker-compose up -d`

# API endpoints
These endpoints allow you to utilize the web application.

## Searching

**POST**
- For Creating an Aircraft
[http://localhost:8000/search/](#search)

***Parameters***
`content-type: application/json`

|     Field     |   Required   |   Type   | Description                   |
| -------------:|:------------:|:--------:|-------------------------------|
|     `year`    | not required |  string  | activity Year                 |
|    `month`    | not required |  string  | activity Month                |
|     `day`     | not required |  string  | activity day                  |
|  `range_from` | not required |  string  | (ISO 8601) date format        |
|   `range_to`  | not required |  string  | (ISO 8601) date format        |
|   `keywprd`   | not required |  string  | activity keyword              |


## Documentation
`Swagger UI` [/docs/](#schema/swagger-ui/)
`redoc` [/redoc/](#schema/redoc/)

# Task Dashboard
* To get the information regarding the tasks already running, visit
http://localhost:5556/
