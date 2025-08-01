"""
Summary: initialize database when first time launch fastapi.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/init_db.py
Author: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 08/01/2025
"""

from datetime import date

from fastapi_songs.database import Base, engine, session_local
from fastapi_songs.models import Song

DEFAULT_SONGS = [
    Song(
        title="There's Nothing Holding Me Back",
        artist="Shawn Mendes",
        release_date=date(2017, 4, 20),
    ),
    Song(title="Jar of Love", artist="Wanting Qu", release_date=date(2012, 1, 1)),
    Song(
        title="Mezase Pokemon Master", artist="Satoshi", release_date=date(1997, 6, 28)
    ),
    Song(
        title="Dancin (KRONO Remix)",
        artist="Aaron Smith",
        release_date=date(2014, 11, 7),
    ),
    Song(
        title="Dancer in the Dark",
        artist="Marc Philippe",
        release_date=date(2018, 5, 10),
    ),
]

Base.metadata.create_all(bind=engine)

db = session_local()

if db.query(Song).count == 0:

    for song in DEFAULT_SONGS:
        db.add(song)

    db.commit()
