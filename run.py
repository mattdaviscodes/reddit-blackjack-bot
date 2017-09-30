import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class Base(object):
    """A base class with some meta field attached."""

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String, nullable=False, default='bot')
    modified_at = Column(DateTime, nullable=True, default=None)
    modified_by = Column(String, nullable=True)

    def __repr__(self):
        return "<{}(id={})>".format(self.__class__.__name__, self.id)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base(cls=Base)


class User(Base):
    __tablename__ = 'users'

    username = Column(String)


if __name__ == '__main__':

    # Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    user = User(username='matt')
    session.add(user)
    session.commit()