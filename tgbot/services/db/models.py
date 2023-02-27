from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TournamentTable(Base):
    __tablename__ = 'table_tournament'

    id = Column(Integer,  primary_key=True)
    team = Column(String, default=None, nullable=True)
    games = Column(Integer, default=None, nullable=True)
    victory = Column(Integer, default=None, nullable=True)
    draw = Column(Integer, default=None, nullable=True)
    defeat = Column(Integer, default=None, nullable=True)
    goals = Column(Integer, default=None, nullable=True)
    missed = Column(Integer, default=None, nullable=True)
    difference = Column(Integer, default=None, nullable=True)
    result = Column(Integer, default=None, nullable=True)
    url = Column(String, default=None, nullable=True)
    up_date = Column(TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now())


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    player = Column(String, default=None, nullable=True)
    role = Column(String, default=None, nullable=True)
    games = Column(Integer, default=None, nullable=True)
    goals = Column(Integer, default=None, nullable=True)
    penalty = Column(Integer, default=None, nullable=True)
    assist = Column(Integer, default=None, nullable=True)
    goalpen = Column(Integer, default=None, nullable=True)
    autogoals = Column(Integer, default=None, nullable=True)
    yellowcards = Column(Integer, default=None, nullable=True)
    redcards = Column(Integer, default=None, nullable=True)
    vrt = Column(Integer, default=None, nullable=True)
    prg = Column(Integer, default=None, nullable=True)
    current_club = Column(String, default=None, nullable=True)
    previous_clubs = Column(String, default=None, nullable=True)
    birthday = Column(String, default=None, nullable=True)
    age = Column(Integer, default=None, nullable=True)
    avatar = Column(String, default=None, nullable=True)
    up_date = Column(TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now())


class About(Base):
    __tablename__ = 'about'
    id = Column(Integer, primary_key=True)
    text = Column(String, default=None, nullable=True)
    up_date = Column(TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now())


class Rules(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    text = Column(String, default=None, nullable=True)
    up_date = Column(TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now())
