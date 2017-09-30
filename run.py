import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()


