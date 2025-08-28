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
### Uvicorn
Uvicorn is an ASGI compatible web server which helps receive browser/client requests and hand over to FastAPI to process requests.<sub>[23]</sub><br >
- Lesson learned: Run FastAPI with uvicorn using Poetry:<br >
- Issue: Bash: `(venv)$ poetry run uvicorn fastapi_songs.main:app --reload --port 8000`
- Reason: Though the tutorial showed command to execute FastAPI with Uvicorn, with Poetry, I was seeking a way to write code in main.py and simply run command `Poetry run fastapi_songs`<br >
- Fix<sub>[24]</sub>:
  ```python
  import uvicorn
  def main():
    """Launch 'poetry run fastapi_songs' at root."""
    uvicorn.run("fastapi_songs.main:app", host="127.0.0.1", port=8000, reload=True)
  ```
  - Explanation: Instead of inputting command, I wrapped the commands into main() with detail, such as uvicorn.run(file string, host=, port=, reeload=) to be simplifed executing command in bash.<sub>[24]</sub><br >
## File: database.py<br >
The database.py declares default database path for SQLite, creates SQLAlchemy engine, session, and declarative_base for further use in models.py, init_db.py, and main.py.<br >
## File: models.py<br >
The models.py inherits Base from database.py and define Song's database structure. The Song class defines the schema which includes __id__, __title__, __artist__, and __release\_date__ for each column and will store in database.<br >
1. Lesson learned: Why do we need declare \_\_tablename\_\_?
- Issue: When following tutorial, I didn't see any variable used \_\_tablename\_\_ once it declared, and I have a question why we should declared it.<br >
- Reason: When we define the data structure that inherits Base, the class (data structure) is mapped to the table in SQLite using \_\_tablename\_\_ by SQLAlchemy. Although SQLAlchemy will auto-generat \_\_tablename\_\_ (default is class name with lowercase and pluralized), declaring when I write the data structure class can potentially prevent naming conflict and model-table mismatch.<sub>[25]</sub><br > 
- Fix: I followed the tutorial and declared `__tablename__ = "songs"`
2. Lesson learned: The update of `sqlalchemy.Column` and `sqlalchemy.ext.declarative.declarative_base()`<br >
- Issue: The `sqlalchemy.Column` and `sqlalchemy.ext.declarative.declarative_base()` is old style in declareing column and declarative base.<br >
- Reason: Althouugh the update style in __SQLAlchemy 2.0+__ is `sqlalchemy.mapped_column` and `sqlalchemy.orm.DeclarativeBase()`, the SQLAlchemy version in tutorial is 1.4.32, so I followed the tutorial to continue use `Column` and `declarative_base()` in this project.<sub>[26][27]</sub><br >
# AWS Elastic Beanstalk
What is Elastic Beanstalk?   Elastic Beanstalk is a __Platform-as-a-Service (PaaS)__ that helps users to deploy their applications on AWS while integrating multiple AWS services. In this project, the main AWS services I used include, __Elastic Compute Cloud (EC2)__, Relational Database Service (RDS)__, and __Elastic Load Balancing (ELB)__. I used Elastic Beanstalk to deploy my apps, and while I selected `db.t3.micro` as my database instance class, the Elastic Beanstalk automatically selected `t3.micro, t3.small` as my EC2 instance type and assigned me EC2 when I deployed applications.<sub>[1][28]</sub><br >
To utilize Elastic Beanstalk, I followed tutorial to install Elastic Beanstalk command line interface (EB CLI).<sub>[29][30][31]</sub> The EB CLI is a tool let me setup, configure, deploy, and manage my Elastic Beanstalk application in linux.<sub>[30]</sub><br >
## Initialize Project
To initialize EB CLI configuration on my project, I ran `eb init`, and CLI prompts:<br >
1. Select Default Region: Tokyo, Japan <br >
2. What's you application name (default: fastapi_songs): press Enter for default <br >
3. What's Platform and Platform Branch: Python 3.11 running on 64-bit Amazon Linux 2023 <br >
4. Codecommit: no (followed the tutorial) <br >
5.SSH to connect to EC2 instance: yes (followed the tutorial)<br >
6. Ask for Keypair: I additionally generated an RSA SSH Keypair and imported as follows: <br >
- Generate RSA SSH Keypair: <br >
```Bash
ssh-keygen -t rsa -b 2048 -f ~/.ssh/eb_keypair
```
- Import the Key pair to EC2: <br >
```Bash
aws ec2 import-key-pair \
  --key-name eb_keypair \
  --public-key-material fileb://~/.ssh/eb_keypair.pub
```
After `eb init`, my project generated `config.yml` under directory `.elasticbeanstalk`. <br >
My `config.yml`: <br >
```Python
branch-defaults:
  main:
    environment: fastapi-songs-dev
    group_suffix: null
global:
  application_name: fastapi_songs
  branch: null
  default_ec2_keyname: aws-eb
  default_platform: Python 3.11 running on 64bit Amazon Linux 2023
  default_region: ap-northeast-1
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  profile: eb-cli
  repository: null
  sc: git
  workspace_type: Application
```
While initializing configuration for my project, I encountered several issues and took note as below: <br >
1. Lesson learned: Order to setup Python, virtual environment, EB CLI.<br >
- Issue: I noticed that there was no Python under my WSL, and the instruction asked to install EB CLI under virtual environment with python.<br >
- Reason: My Python was installed under Windows, and this is the first project I started under WSL which neither Python and virtual environment were installed.<br >
- Fix: I chose to install pyenv which provide both Python and venv.<sub>[32]</sub> After that, I further installed EB CLI under virtual environment.<br >
2. Lesson learned: When I `eb init` and selected aws default region, the CLI prompts:<br >
     > You have not yet set up your credentials or your credentials are incorrect<br >
     > You must provide your credentials.<br >
     > (aws-access-id):<br >
- Issue: The Elastic Beanstalk CLI (eb) cannot find my AWS credentials.<br >
- Reason: I didn't setup my aws access key and secret<br >
- Fix: I have to create an AWS __IAM user__ with access key in aws console.<sub>[33]</sub> To do that:<br >
   1. I went to AWS console: https://console.aws.amazon.com/ <br >
   2. Selected my account on _top right_ and selected __Security credentials__ <br >
   3. On left sidebar, I selected __Dashboard__ -> __Access Management__ -> __Users__ <br >
   4. I selected __Create User__, type User name:  _eb\_cli\_user_ -> __Next__ <br >
   5. In Permission Options, I selected __Attach policies directly__. Then search and add `AdministratorAccess-AWSElasticBeanstalk`, `AmazonEC2FullAccess` -> __Next__ -> __Create user__ <br >
   6. I selected _eb\_cli\_user_ and selected __Create access key__ in Summary<br >
   7. I selected __Command Line Interface (CLI)__ -> checked __Confirmation__ -> __Next__ <br >
   8. I left _Set description tag - optional_ empty -> __Create access key__ <br >
   9. After that, I got back to linux and `aws configure` and input: <br >
      > AWS Access Key ID [None]: <access-key-id> <br >
      > AWS Secret Access Key [None]: <secret-access-key> <br >
      > Default region name [None]: <br >
      > Default output format [None]: json <br >
   10. Then I checked access key, secret key, and region setting by `aws configure list` <br >
   11. [optional]: To refresh aws cli, I `rm -rf ~/.aws/cli/cache` and restart shell by `exec $SHELL`
3. Lesson learned: After I input my AWS IAM user and access key, then I `eb init`, and the CLI prompts:<br >
   > not authorized to perform: s3:PutBucketOwnershipControls on resource: <br >
   > "arn:aws:s3:::elasticbeanstalk" because no identity-based policy allows the s3:PutBucketOwnershipControls action <br >
- Issue : Elastic Beanstalk uses an S3 bucket to store my app versions and environment data, but it failed <br >
- Reason: My IAM user (eb_cli_user) does not have permission to creates or configures S3 bucket.<br >
- Fix: I have to create permissions `s3:PutBucketOwnershipControls` at:<sub>[34]</sub><br >
   1. AWS IAM console: https://console.aws.amazon.com/iam
   2. On left sidebar, I selected __Dashboard__ -> __Access Management__ -> __Users__ <br >
   3. I selected _eb\_cli\_user_ and in __Permissions policies__, I selected __Add permissions__ -> __Create inline policy__ <br >
   4. I selected __JSON__ in _Policy editor_ and added:<br >
   ```JSON
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Action": [
           "s3:PutBucketOwnershipControls"
         ],
         "Effect": "Allow",
         "Resource": "arn:aws:s3:::elasticbeanstalk-*"
       }
     ]
   }
   ```
   5. I clicked __Next__ and added Policy name `s3PutBucketOwnershipControls` -> __Create policy__ <br >
## Create Project Environment on AWS and deploy the project <br >
To create environment on AWS and deploy my project, I ran `eb create`, and CLI prompts: <br >
1. Enter Environment Name (default: fastapi-songs-env): press Enter for default <br >
2. Enter DNS CNAME prefix (default: fastapi-songs-dev): press Enter for default <br >
3. Select a load balancer type: select application<br >

While creating environment for my project, I encountered several issues and noted them as below: <br >
1. Lesson learned: __AWS Linux log checking__ <sub>[35][36]</sub><br >
   - Issue:  My project deployed failed after running `eb create`<br >
   - Reason: Error log - __ERROR Instance deployment failed. For details, see 'eb-engine.log'.__ <br >
   - Fix: I connected to AWS Linux to checked error message in 'eb-engine.log' as follows: <br >
      1. `eb list`   #list running environments <br >
      2. `eb ssh`    #access AWS Linux by SSH <br >
      3. `sudo less /var/log/eb-engine.log`   #open and read eb-engine.log <br >
2. Lesson learned: First-time SSH confirmation to a new EC2 instance <br >
   - Issue: When first using SSH to access Amazon Linux - EC2 instance (`eb ssh`), EB CLI displayed: <br >
   > INFO: Running ssh -i /home/.ssh/aws-eb -o IdentitiesOnly yes ec2-user@0.0.0.0 The authenticity of host can't be established. This SSH key is not known by any other names. Are you sure you want to continue connecting (yes/no/[fingerprint])?
   - Reason: This is a warning shown when using SSH connecting to a new EC2 instance for the first time<br >
   - Fix: I type `Yes` and pressed Enter which added EC2 server's fingerprint to my `~/.ssh/known_hosts`, allowiing automatic trust for future connections to EC2 instance. <br >
3. Lesson learned: __Profile__ and __requirements.txt__ files are required when running `eb create` <br >
   - Issue: During `eb create`, EB logs showed error message as follows: <br >
   > [WARN] failed to read file /var/pids/web.pid with error: open /var/pids/web.pid: no such file or directory <br >
   > [ERROR] update processes [web healthd cfn-hup nginx] pid symlinks failed with error failed to read file /var/pids/web.pid after 6 attempts <br >
   - Reason: EB expected my app started __web server process__ and write its __PID__ to __/var/pids/web.pid__ <br >
   - Fix: I created Procfile and generated requirements.txt as follows:<sub>[37][38]</sub> <br >
     1. Procfile: <br >
      ```Vbnet
      web: gunicorn src.fastapi_songs.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
      ```
     2. requirements.txt: <br >
      ```Bash
      poetry run python -m pip freeze > requirements.txt
      ```
4. Lesson learned: A new EC2 instance starts as an empty Linux system, and we have to install all packages we need to match what we have in local project. <br > 
   - Issue:
     > [ERROR] An error occurred during execution of command [app-deploy] - [InstallDependency]. Stop running the command. Error: fail to install dependencies with requirements.txt file with error Command /var/app/venv/staging-LQM1lest/bin/pip install -r requirements.txt failed with error exit status 1. Stderr: ERROR: Error [Errno 2] No such file or directory: 'git' while executing command git version ERROR: Cannot find command 'git' - do you have 'git' installed and in your PATH?
   - Reason: The EB deployment failed because it tried to install my project using Git SSH dependency from `requirements.txt`, but the new EC2 Linux instance doesn't have Git installed. <br >
   - Fix: The EB deployment doesn't need Git. The proper workflow is: develop project locally with Git -> commit, push, and create a pull request -> deploy to EC2. The quick fix is comment out the Git SSH dependency in `requirements.txt`:
     ```Bash
     -e git+ssh://git@github.com/raylai-proj/fastapi_songs.git
     ```
     and redeploy by `eb deploy`.<sub>[39]</sub> <br >
     
## EC2 SSH <br >
What is EC2 SSH? EC2 is Elastic Compute Cloud instance (linux operating system) which I selected to run my project in AWS. SSH is Secure Shell which is encrypted network protocol for remote access to servers. EC2 SSH refers to using SSH to remotely connect to the AWS EC2 instance (Amazon Linux), so I can run commands, install packages, and do trouble shootings.<sub>[40]</sub> <br >
## DNS CNAME Prefix <br >
What is DNS CNAME Prefix? When deploying app delivered by the project on aws, Elastic Beanstalk will create a DNS name with CNAME as prefix e.g., `<CNAME-prefix>.<region>.elasticbeanstalk.com`. For example, if I choose __fastapi-songs-dev__ as my CNAME, my DNS would be:
```Bash
fastapi-songs-dev.<region>.elasticbeanstalk.com
```
Therefore, the DNS CNAME prefix is the subdomain name for the EB environment’s default public URL.<sub>[41]</sub> <br >
## Load Balancer
What is Load Balancer? The Elastic Load Balancer is an aws service that helps distribute network traffic to prevent traffic bottlenecks. In my project, I chose Application Load Balancer which helps distribute income network traffic between EC2 instances, containers, and IP addresses ensuring each registered node remains healthy.<sub>[42][43][44]</sub> <br >
## Configuring Environment from `eb create` and `eb deploy` <br >
The `eb create` creates an environment on AWS for deploying my project, and I have to configure the environment, so the EC2 instance can locate my project during deployment.<br >
1. Define __PYTHONPATH__ and __WSGIPath__ to let EC2 instance locate application entry point during deployment:<br >
.ebextensions/01_fastapi.config
```yaml
option_settings:
    aws:elasticbeanstalk:application:environment:
        PYTHONPATH: "/var/app/current/src:$PYTHONPATH"
    aws:elasticbeanstalk:container:python:
        WSGIPath: "src/fastapi_songs/main:app"
```
2. Define __container\_commands__ for database initialization: <br >
.ebextensions/01_fastapi.config
```yaml
container_commands:
    01_initdb:
        command: |
            source /var/app/venv/*/bin/activate
            cd /var/app/current
            PYTHONPATH=./src python3 src/fastapi_songs/init_db.py
        leader_only: true
```
3. Add Procfile commands for EB to start FastAPI application on the web server. <br >
Procfile
```Procfile
web: gunicorn src.fastapi_songs.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
```
1. Lesson learned: Python __src layout__ mismatch in optional settings in 01_fastapi/config <br >
   - Issue: <br >
   ```Bash
   [ERROR] Command 01_initdb (source /var/app/venv/*/bin/activate && python3 src/fastapi_songs/init_db.py) failed <br >
   ```
   - Reason: During `eb deploy`, EC2 failed in executing command `01_init_db` when deploying app. <br >
   - Fix: Direct testing in EC2 to further find the issue: <br >
   ```Bash
   (staging-LQM1lest) [ec2-user@ip- staging]$ python3 src/fastapi_songs/init_db.py
   ```
2. Lesson learned: When using src layout, I have to include `PYTHONPATH = ./src`, so Python can resolve fastapi_songs/ as a module.<sub>[45]</sub> <br >
   - Issue:<br >
   > Traceback (most recent call last): File "/var/app/staging/src/fastapi_songs/init_db.py",
   > line 12, in <module> from fastapi_songs.database import Base, engine, session_local ModuleNotFoundError: No module named 'fastapi_songs'
   - Reason: When using the __src layout__, Python doesn’t automatically treat `src/` as the package root on EC2. <br >
   - Fix: Add `PYTHONPATH = ./src` in 01_init_db command:
     ```yaml
     container_commands:
       01_initdb:
           command: |
               source /var/app/venv/*/bin/activate
               cd /var/app/current
               PYTHONPATH=./src python3 src/fastapi_songs/init_db.py
           leader_only: true
     ```
## PYTHONPATH <br >
Does `PYTHONPATH` in `PYTHONPATH: "/var/app/current/src:$PYTHONPATH"` in _.extensions/01_fastapi_songs.config_ search for Python interpreter or files in the project that has entry point ? `PYTHONPATH` is __not for finding Python interpreter__. Instead, it's used by Python to determine __where to search for modules and packages__ when running Python code on EC2.<sub>[45][46]</sub><br >

## WSGIPath <br >
1. Why does Elastic Beanstalk use `WSGIPath` in _.extensions/01_fastapi_songs.config_? Elastic Beanstalk’s Python platform historically expects WSGI applications (like Flask or Django), and that's why the variable name is WSGIPath, but it’s just the name of the key that EC2 uses to know where to find the application entry point, and it doesn’t mean the app must strictly be WSGI. <sub>[47]</sub><br >
2. How does FastAPI (ASGI) work with WSGIPath? <sub>[46][48][49]</sub><br >
   - Although FastAPI is ASGI, ASGI servers like Uvicorn or Gunicorn+Uvicorn workers can still be launched by EB.<br >
   - EB uses WSGIPath as a pointer which points to "src/fastapi_songs/main:app" to find the app entry point. <br >
   - Finally, I configure __Procfile__ to instruct EB to run Gunicorn (which is WSGI) + uvicorn (which is ASGI and run fastapi_songs). <br >

## Procfile <br >
What is Procfile and what does a Procfile do? __Procfile__ is a text file with command, and the EB run the command when starting my web app. The Procfile defines how the web server start. <sub>[49][50][51]</sub><br >

## Gunicorn <br >
What is Gunicorn and what does it do? Gunicorn (Green unicorn) is a Python WSGI HTTP Server. In my project, Gunicorn is supported by Elastic Beanstalk as a web WSGI application and can be used to support FastAPI and Uvicorn which enable ASGI compatibility.<sub>[48][50]</sub> In my Procfile: <br >
```Procfile
web: gunicorn src.fastapi_songs.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
```
When EB started the web app server, it started gunicorn and used 4 concurrent Uvicorn workers to run my app in `src/fastapi_songs/maiin:app`. <br >

## Configuring Database <br >
In addition to SQLite, the tutorial also provided PostgreSQL and AWS RDS Postgres for database deployment. <br >
### local postgreSQL Setup: <br >
1. Start a new docker container with postgreSQL server:<sub>[52]</sub> <br >
```Bash
docker run -d \
--name fastapi-songs-postgres \
-e POSTGRES_USER=fastapi-songs \
-e POSTGRES_PASSWORD=complexpassword123 \
-e POSTGRES_DB=fastapi-songs \
-p 5432:5432 \
postgres
```
2. Check if container is running:<sub>[53]</sub> <br >
```Bash
docker ps -f name=fastapi-songs-postgres
```
3. Add postgreSQL database info in database.py: <br >
```Python
USER = "fastapi-songs"
PW = "complexpassword123"
HOST = "localhost"
PORT = "5432"
DATABASE = "fastapi-songs"
POSTGRESQL_URL = f"postgresql://{user}:{pw}@{host}:{port}/{database}"
engine = create_engine(POSTGRESQL_URL)
session_local = sessionmaker(bind=engine, autoflush=False)
```
4. Add `psycopg2-binary in poetry: <br >
```Bash
poetry add --group dev "psycopy2-binary=2.9.3"
```
5. Run the project in local with postgreSQL: <br >
```Bash
poetry run python src/fastapi_songs/init_db.py
poetry run fastapi_songs
```
1. Lesson learned: Docker has container with postgreSQL installed: <br >
   - Issue: I want to quickly use postgreSQL. <br >
   - Reason: Docker can start a new container with postgreSQL server. <br >
   - Fix: Install Docker:<sub>[54]</sub> <br >
   ```Bash
   sudo apt install gnome-terminal
   sudo apt-get update
   sudo apt-get install -y ./docker-desktop-amd64.deb
   ```
2. Lesson learned: Unable to install psycopg2-binary 2.9.3 <br >
   - Issue: <br >
   ```Bash
   Error: pg_config executable not found. | | pg_config is required to build psycopg2 from source.
   Please add the directory | containing pg_config to the $PATH or specify the full executable path
   ```
   - Reason: To install `psycopg2-binary`, The prerequest files `libpq-dev python3-dev build-essential` must install first:<sub>[55]</sub> <br >
   - Fix: <br >
   ```Bash
   sudo apt-get update
   sudo apt-get install -y libpq-dev python3-dev build-essential
   ```

### Docker<br >
What is Docker and what does it do? Docker is a lightweight tool provides application independency and database support. Docker allows developers to isolate different app environments, preventing software and library version conflicts. In addition, Docker provides containers with PostgreSQL server pre-installed, so developers can use it directly without additional database setup.<sub>[56]</sub><br >

### PostgresSQL<br >
What is PostgreSQL and what does it do? PostgreSQL is a open source object-relational database system which works great with FastAPI application.<sub>[57][58]</sub><br >

### psycopg2-binary<br >
What is pyscopg2-binary and what does it do?<br >
> __Psycopg__ is a __PostgreSQL__ adapter for the __Python__ programming language. It is a wrapper for the __libpq__, the official PostgreSQL client library.<sub>[55]</sub><br >
### AWS RDS Postgres Setup:<br >
1. `eb console` -> left sidebar select __Configuration__ -> in __Networking and database__, click __Edit__<br >
2. Configure database info: <br >
   - Engine: Postgres<br >
   - Instance Class : db.t3.micro<br >
   - Storage: 5 GB<br >
   - Username: <username><br >
   - Password: <password><br >
   - Availability: low<br >
   - Database deletion policy: Create Snapshot<br >
3. After __Apply__, the environment will gear with postgreSQL, and it will automatically generate environment variables in os.environ: <br >
   - RDS_USERNAME<br >
   - RDS_PASSWORD<br >
   - RDS_HOSTNAME<br >
   - RDS_PORT<br >
   - RDS_DB_NAME<br >
4. Add environment variables in database.py:<br >
```Python
try:
    user = os.environ["RDS_USERNAME"]
    pw = os.environ["RDS_PASSWORD"]
    host = os.environ["RDS_HOSTNAME"]
    port = os.environ["RDS_PORT"]
    database = os.environ["RDS_DB_NAME"]

except Exception as e:
    print(e)

finally:
    postgersql_url = f"postgresql://{user}:{pw}@{host}:{port}/{database}"
    engine = create_engine(postgersql_url)
```

1. Lesson learned: The __auto-generated__ environment variables will detached after next `eb deploy`.<br >
   - Issue: <br >
   ```Bash
   'RDS_USERNAME' Traceback (most recent call last):
   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1),
   port 5432 failed: Connection refused Is the server running on that host and accepting TCP/IP connections?
   ```
   - Reason: Elastic Beanstalk may detach __auto-generated__ environment variables once `eb deploy` failed or redeploy environment. <br >
   - Fix: Manually setup environment variables:<sub>[59]</sub><br >
      1. `eb console` -> left sidebar select __Configuration__ -> in __Updates, monitoring, and logging __, click __Edit__<br >
      2. In __Environment properties__, click __Add environment property__ and fill in:<br >
         - RDS_USERNAME: `eb console` -> __Configuration__ -> Networking and database -> __Edit__ -> Username<br >
         - RDS_PASSWORD: `eb console` -> __Configuration__ -> Networking and database -> __Edit__ -> Password<br >
         - RDS_HOSTNAME: https://console.aws.amazon.com/rds -> __DB Instances__ -> Connectivity & security -> Endpoint<br >
         - RDS_PORT: https://console.aws.amazon.com/rds -> __DB Instances__ -> Connectivity & security -> Port<br >
         - RDS_DB_NAME: `eb console` -> __Configuration__ -> Networking and database -> Database username<br >

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
[23] [What is the purpose of Uvicorn?](https://stackoverflow.com/questions/71435960/what-is-the-purpose-of-uvicorn)<br >
[24] [How to run FastAPI application from Poetry?](https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry)<br >
[25] [SQLAlchemy 2.0 Documentation - The table, or other from clause object](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#the-table-or-other-from-clause-object)<br >
[26] [SQLAlchemy 2.0 Documentation - Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table)<br >
[27] [SQLAlchemy 2.0 Documentation - sqlalchemy.orm.DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase)<br >
[28] [What is AWS Elastic Beanstalk?](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)<br >
[29] [aws-elastic-beanstalk-cli-setup](https://github.com/aws/aws-elastic-beanstalk-cli-setup)<br >
[30] [awsebcli 3.25](https://pypi.org/project/awsebcli/)<br >
[31] [Installing or updating to the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)<br >
[32] [Github - pyenv](https://github.com/pyenv/pyenv)<br >
[33] [How do I get my AWS Access ID and Secret Key for EB CLI?](https://www.reddit.com/r/aws/comments/zfr0m6/how_do_i_get_my_aws_access_id_and_secret_key_for/)<br >
[34] [Managing Elastic Beanstalk user policies](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.iam.managed-policies.html)<br >
[35] [Troubleshooting your Elastic Beanstalk environment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/troubleshooting.html)<br >
[36] [[Viewing logs from Amazon EC2 instances in your Elastic Beanstalk environment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html)]<br >
[37] [Buildfile and Procfile](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.build-proc.html)<br >
[38] [Setting up your Python development environment for Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-development-environment.html)<br >
[39] [eb deploy](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-deploy.html)<br >
[40] [eb ssh](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-ssh.html)<br >
[41] [eb create](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-create.html)<br >
[42] [What is Load Balancing?](https://aws.amazon.com/what-is/load-balancing/)<br >
[43] [What is an Application Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)<br >
[44] [AWS Elastic Load Balancer: Overview And Types With Practical](https://medium.com/%40Raghvendra_Tyagi/aws-elastic-load-balancer-overview-and-types-with-practical-c214cbdfdd9b)<br >
[45] [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)<br >
[46] [Using the Elastic Beanstalk Python platform](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-container.html)<br >
[47] [Platform specific options](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python)<br >
[48] [Server Workers - Uvicorn with Workers](https://fastapi.tiangolo.com/deployment/server-workers/)<br >
[49] [Uvicorn - Deployment](https://www.uvicorn.org/deployment/)<br >
[50] [Configuring the WSGI server with a Procfile on Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-configuration-procfile.html)<br >
[51] [Advanced environment customization with configuration files (.ebextensions)](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html)<br >
[52] [docker container run](https://docs.docker.com/reference/cli/docker/container/run/)<br >
[53] [docker container ls](https://docs.docker.com/reference/cli/docker/container/ls/)<br >
[54] [Install Docker Desktop on Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)<br >
[55] [Psycopg 2.9.10 documentation - Build prerequisites](https://www.psycopg.org/docs/install.html#build-prerequisites)<br >
[56] [What is Docker?](https://docs.docker.com/get-started/docker-overview/)<br >
[57] [PostgreSQL](https://www.postgresql.org/)<br >
[58] [What is PostgreSQL?](https://www.digitalocean.com/community/tutorials/what-is-postgresql)<br >
[59] [Environment variables and other software settings](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html)<br >

