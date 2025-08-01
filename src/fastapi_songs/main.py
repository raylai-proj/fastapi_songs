"""
Summary: main.py is FastAPI entry with all pages.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/main.py
Name: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 07/31/2025
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Fastapi website root entry."""
    return {"name": "FastAPI_songs"}


def main():
    """Launch 'poetry run fastapi_songs' at root."""
    uvicorn.run("fastapi_songs.main:app", host="127.0.0.1", port=8000, reload=True)
