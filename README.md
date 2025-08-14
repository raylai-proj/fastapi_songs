# Using AWS Elastic Beanstalk to deploy Fastapi app: Fastapi_songs
# Introduction
This is a personal workshop following tutorial<sub>[1]</sub>, implementing a FastAPI application (_FastAPI_songs_) and deploying it to AWS using Elastic Beanstalk. While following the tutorial, I also took notes on every issue I encountered and the lessons I learned. <br >

# Fastapi Songs Application
The `fastapi_songs` application has two simple pages (`127.0.0.1:8000` and `127.0.0.1:8000/songs/`), and both returning data in JSON format. The entry page simply returns _name_ and _Fastapi_ key-value pair, while the _/songs/_ page returns preset song list with _title_, _artist_, and _release_ _date_ fields. The application serves as a sample for deployment on AWS, and its project structure is well-suited for use as a reference for common usage pattern.<br >
## Structure
fastapi_songs/<br >
.<br >
├── src<br >
│   └── fastapi_songs<br >
│       ├── \_\_init\_\_.py<br >
│       ├── database.py<br >
│       ├── init_db.py<br >
│       ├── main.py<br >
│       └── models.py<br >
├── .ebextensions<br >
│   └── 01_fastapi.config<br >
├── .elasticbeanstalk<br >
│   └── config.yml<br >
└── README.md<br >
## File: main.py
### sqlalchemy
### SQLite
### uvicorn
## File: database.py
## File: models.py
# AWS Elastic Beanstalk
## SSH
## DNS CNAME Prefix
## Load Balancer
## gunicorn
## Docker
## PostgresSQL
## psycopg2-binary
## AWS RDS Postgres
# Lessons Learned
## os
## RDS variables

# Reference
[1] [Deploying a FastAPI Application to Elastic Beanstalk](https://testdriven.io/blog/fastapi-elastic-beanstalk/#environment-variables)<br >
