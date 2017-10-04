import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'), echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

