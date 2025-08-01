"""
Summary: main.py is FastAPI entry with all pages.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/main.py
Name: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 07/31/2025
"""

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import Base, engine, session_local
from .models import Song

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Get session to interact with db."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """Fastapi website root entry."""
    return {"name": "FastAPI_songs"}


@app.get("/songs/")
def display_songs(db: Session = Depends(get_db)):
    """Show song list."""
    return db.query(Song).all()


def main():
    """Launch 'poetry run fastapi_songs' at root."""
    uvicorn.run("fastapi_songs.main:app", host="127.0.0.1", port=8000, reload=True)
