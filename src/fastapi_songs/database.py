"""
Summary: database.py declare engine, session, and declarative base for sqlalchemy to use.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/database.py
Author: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 08/01/2025
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "default.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
