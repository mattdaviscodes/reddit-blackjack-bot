import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from . import Session


class Base(object):
    """A base class with some meta field attached."""

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String, nullable=False, default='bot')
    modified_at = Column(DateTime, nullable=True, default=None)
    modified_by = Column(String, nullable=True)


    # CRUD methods below from https://github.com/sloria/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/database.py
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        session = Session()
        session.add(self)
        if commit:
            session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        session = Session()
        session.delete(self)
        return commit and session.commit()

    def __repr__(self):
        return "<{}(id={})>".format(self.__class__.__name__, self.id)


Base = declarative_base(cls=Base)

user_achievements = Table('user_achievements', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('achievement_id', ForeignKey('achievements.id'), primary_key=True)
)


class User(Base):
    """Model to represent users.

    Tempted to call this Player, but I might want to create users for
    people who haven't started a game yet -- if they just issue a
    non game-starting command.
    """
    __tablename__ = 'users'

    username = Column(String, unique=True)
    credits = Column(Integer)

    games = relationship('Game', back_populates='user')
    achievements = relationship('Achievement',
                                secondary=user_achievements,
                                back_populates='users')

    def charge(self, credits):
        """Reduce user's credits.

        :param credits: Integer credits to reduce self.credits by
        :return:
        """
        self.update(credits=self.credits-credits)

    def pay(self, credits):
        """Increase user's credits.

        :param credits: Integer credits to increase self.credits by
        :return:
        """
        self.update(credits=self.credits+credits)


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
    state = Column(String, nullable=False)
    bet = Column(Integer, nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True, default=None)

    user = relationship('User', back_populates='games')


class Achievement(Base):
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
    __tablename__ = 'achievements'

    name = Column(String, nullable=False)
    description = Column(String)

    users = relationship('User',
                         secondary=user_achievements,
                         back_populates='achievements')


