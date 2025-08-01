"""
Summary: initialize database when first time launch fastapi.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/init_db.py
Author: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 08/01/2025
"""

from fastapi_songs.database import Base, engine, session_local

Base.metadata.create_all(bind=engine)

db = session_local()
