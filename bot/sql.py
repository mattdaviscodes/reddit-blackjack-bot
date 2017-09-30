import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    """A base class with some meta field attached."""

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String, nullable=False, default='bot')
    modified_at = Column(DateTime, nullable=True, default=None)
    modified_by = Column(String, nullable=True)

    def __repr__(self):
        return "<{}(id={})>".format(self.__class__.__name__, self.id)


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base(cls=Base)


class User(Base):
    """Model to represent users.

    Tempted to call this Player, but I might want to create users for
    people who haven't started a game yet -- if they just issue a
    non game-starting command.
    """
    __tablename__ = 'users'

    username = Column(String)


class Game(Base):
    """Model to represent hands of blackjack.

    Fields:
        start date
        end date
        player (FK)
        game state (blackjack notation)
        bet
    """
    __tablename__ = 'games'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True, default=None)

    user = relationship('User', back_populates='games')


class Achievement:
    """Lookup table for player achievements.

    Fields:
        name
        description
        bounty -- point award for earning achievement?

    Possible:
        hit blackjack
        pushed on a blackjack
        hit 21 on doble down
        stayed on <10 and won
        hit on 19> and didn't bust
    """
    pass


class UserAchievement:
    """Mapping table -- users to achievements

    Not sure if this is required. If sqlalchemy works the same without Flask
    as it does with Flask, then all I need is the two tables, and sqlalchemy
    will take care of the relationship for me.
    """
    pass




