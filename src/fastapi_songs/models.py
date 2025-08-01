"""
Summary: models.py defines Song table inherit from Base.

Reference: https://github.com/duplxey/fastapi-songs/blob/master/models.py
Author: Chun-Juei Lai
Email: chunjueilai@gmail.com
Date: 08/01/2025
"""

from database import Base
from sqlalchemy import Column, Date, Integer, String


class Song(Base):
    """Define Song table inherit declarative_base."""

    __tablename__ = "songs"
    id = Column(type_=Integer, primary_key=True)
    title = Column(type_=String(128), nullable=False)
    artist = Column(type_=String(128), nullable=False)
    release_date = Column(type_=Date, nullable=False)
