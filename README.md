# Spinning Up On Local System
- Download  and install docker from www.docker.com
- CD into the root folder of the application
- On your terminal, run `docker-compose build`
- On your terminal, run `docker-compose up -d`
- When done, to shut it down, run `docker-compose down -v`

# API endpoints
These endpoints allow you to utilize the web application.

## Searching

**POST**
- For Searching Data
[http://localhost:1337/search/](#search)

***Parameters***
`content-type: application/json`

|     Field     |   Required   |   Type   | Description                   |
| -------------:|:------------:|:--------:|-------------------------------|
|    `lookup`   | not required |  string  | "inclusive" or "exclusive"    |
|     `year`    | not required |  string  | activity Year                 |
|    `month`    | not required |  string  | activity Month                |
|     `day`     | not required |  string  | activity day                  |
|   `location`  | not required |  string  | activity location             |
|  `range_from` | not required |  string  | (ISO 8601) date format        |
|   `range_to`  | not required |  string  | (ISO 8601) date format        |
|   `keyword`   | not required |  string  | activity keyword              |


## Manually Indexing

**POST**
- For Manually Indexing for a Day
[http://localhost:1337/manually-index/](#manually-index)

***Parameters***
`content-type: application/json`

|     Field     |   Required   |   Type   | Description                   |
| -------------:|:------------:|:--------:|-------------------------------|
|     `date`    |   required   |  string  | (ISO 8601) date format        |


## Documentation
`Swagger UI` [/docs/](#schema/swagger-ui/)
`redoc` [/redoc/](#schema/redoc/)

# Task Dashboard
* To get the information regarding the tasks already running, visit
http://localhost:1337/

# Live Server
`ec2-18-222-120-235.us-east-2.compute.amazonaws.com`