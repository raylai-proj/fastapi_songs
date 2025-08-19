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
The main.py register several instances and functions as following:<br >
1. app = FastAPI(): The FastAPI() instance which allows functions decorated by @app become FastAPI.<br >
2. @app.get("/") <br >
   def root():<br >
  The app root entry ("/") for testing and returning JSON {"name": "FastAPI_songs"}.<br >
3. @app.get("/songs/") <br >
  def display_songs(db: Session=Depends(get_db)): <br >
  The app display_songs entry ("/songs/") to query preset songs list from database.<br >
  - Lessons learned - `Depends(get_db)`: `Depends` is in Dependency Injection System in FastAPI which is a shortcut to call `get_db()` and return session as a function argument.<sub>[2]</sub><br >
4. def get_db(): <br >
  The get_db function starts a database session to handle connection and interaction between app and database.<sub>[3]</sub><br >
  - Lessons learned - `yield db`: in addition to return db to request handler, `yield` pause and give control to request handler, and continue the program after it done.<sub>[4][5]</sub><br >
   
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
[2] [FastAPI - Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)<br >
[3] [SQLAlchemy 2.0 Documentation - Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)<br >
[4] [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/#understanding-the-python-yield-statement)<br >
[5] [Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)<br >
