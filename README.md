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
  - Lessons learned - `db: Session=Depends(get_db)`: `db: Session` is argument name and type is Session object, and `Depends` is in Dependency Injection System in FastAPI which is a shortcut to call `get_db()` and return session as the function argument db.<sub>[2]</sub><br >
  In summary, `:` means __type__, `=` means __default value__, `Depends` is tool function in FastAPI.<sub>[2][3]</sub><br >
4. def get_db(): <br >
  The get_db function starts a database session to handle connection and interaction between app and database.<sub>[4]</sub><br >
  - Lessons learned - `yield db`: in addition to return db to request handler, `yield` pause and give control to request handler, and continue the program after it done.<sub>[5][6]</sub><br >
   
### SQLAlchemy
SQLAlchemy is a Python library for working with database.<sub>[7]</sub> It includes several important tools for establishing connections and manipulating data in databases. Some key functions and classes include:<br >
1. `sqlalchemy.create_engine()`: Establish a call as bridge to database. This includes creating a dialect to the database and a pool for establishing connection to local host.<sub>[8]</sub><br >
2. `sqlalchemy.orm.sessionmaker()`: The orm stands for Object-Relational Mapping. This mapping maps database table (SQL) to Python classes and records (rows) into Python object. The sessionmaker generates a session object to interact (add, commit, query, and close) with the database.<sub>[9]</sub><br >
- Lesson learned - SQLAlchemy connection workflow: create engine -> create session -> interact with database<br >
3. `sqlalchemy.ext.declarative.declarative_base()`: The declarative_base declares a base class to let us inherit it and customized our database structure.<sub>[11]</sub><br >
- Lesson learned - SQLAlchemy create SQL table workflow:<sub>[10][11][12]</sub><br >
     (1) declare base class<br >
     (2) define customized class and inherit base class (register as a table model)<br >
     (3) using `metadata.create_all()` to check classes being defined and convert to SQL `CREATE TABLE` statements and create tables<br >

In addition, SQLAlchemy provides schema related classes such as `Column`, `Date`, `Integer`, `String` to help define and regulate database structures.<sub>[13][14][15]</sub><br >
### SQLite
- Lesson learned - SQLite database URL setting:<br >
- Issue: After setting up the app, I noticed the init_db.py didn't create preset data into database.<br >
- Reason: I realized the project structure I used is __src layout__ compare to __flat layout__ which the tutorial provided. Because the SQLite used __relative path__, src layout turned out init_db.py created database which `display_songs()` in main.py couldn't reach.<br >
- Fix: I changed from __relative path__ to __absolute path__ for SQLite.<br >
  - Original SQLite path: `"sqlite:///./default.db"`<br >
  - Explanation: The `"sqlit:///"` is sqlite path prefix used in SQLAlchemy. The `"./"` means current directory.<sub>[16]</sub><br >
  - Fixed SQLite path:<br >
  ```python
  import os
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  DB_PATH = os.path.join(BASE_DIR, "default.db")
  SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
  ```
  - Explanation:<br >
  1. `__file__` is a python built-in variable which stores current module path when being executed.<sub>[17][18]</sub><br >
  2. `os.path.abspath(__file__)` returns executed module absolute path. Because `__file__` can be relative or absolute path depends on Python version, I used `os.path.abspath(__file__)` to make sure we get absolute path.<sub>[19]</sub><br >
  3. `os.path.dirname(current_path)` returns directory name of current path which means it returns path one up layer.<sub>[20][21]</sub><br >
  4. `os.path.join(var1,...)` can receive any number path variables and add them up as a path sequentially with "/" between each of them. If one path variable is absolute path (has `/` or `C:\`), the path variables before the absolute path will be discarded.<sub>[22]</sub><br >
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
[2] [Explicitly define datatype in a Python function](https://www.geeksforgeeks.org/python/explicitly-define-datatype-in-a-python-function/)<br >
[3] [FastAPI - Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)<br >
[4] [SQLAlchemy 2.0 Documentation - Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)<br >
[5] [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/#understanding-the-python-yield-statement)<br >
[6] [Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)<br >
[7] [SQLAlchemy 2.0 Documentation - Overview](https://docs.sqlalchemy.org/en/20/intro.html#documentation-overview)<br >
[8] [SQLAlchemy 2.0 Documentation - Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)<br >
[9] [SQLAlchemy 2.0 Documentation - Session API](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker)<br >
[10] [SQLAlchemy 2.0 Documentation - Declarative API](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/api.html#module-sqlalchemy.ext.declarative)<br >
[11] [SQLAlchemy 2.0 Documentation - Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.metadata)<br >
[12] [SQLAlchemy 2.0 Documentation - Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-metadata)<br >
[13] [SQLAlchemy 2.0 Documentation - Describing Databases with MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)<br >
[14] [SQLAlchemy 2.0 Documentation - The Type Hierarchy](https://docs.sqlalchemy.org/en/20/core/type_basics.html)<br >
[15] [Column and Data Types in SQLAlchemy](https://www.geeksforgeeks.org/python/column-and-data-types-in-sqlalchemy/)<br >
[16] [SQLAlchemy engine absolute path URL in windows](https://stackoverflow.com/questions/19260067/sqlalchemy-engine-absolute-path-url-in-windows)<br >
[17] [what does the __file__ variable mean/do?](https://stackoverflow.com/questions/9271464/what-does-the-file-variable-mean-do)<br >
[18] [PEP 451 – A ModuleSpec Type for the Import System](https://peps.python.org/pep-0451/)<br >
[19] [os.path — Common pathname manipulations - os.path.abspath(path)](https://docs.python.org/3/library/os.path.html#os.path.abspath)<br >
[20] [os.path — Common pathname manipulations - os.path.dirname](https://docs.python.org/3/library/os.path.html#os.path.dirname)<br >
[21] [Python | os.path.dirname() method](https://www.geeksforgeeks.org/python/python-os-path-dirname-method/)<br >
[22] [os.path — Common pathname manipulations - os.path.join(path, /, *paths)](https://docs.python.org/3/library/os.path.html#os.path.join)<br >

