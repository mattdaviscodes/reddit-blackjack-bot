import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'), echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
