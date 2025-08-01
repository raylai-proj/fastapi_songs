"""
Summary: database.py declare engine, session, and declarative base for sqlalchemy to use.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/database.py
Author: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 08/01/2025
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./default.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_local = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
