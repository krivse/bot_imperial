from sqlalchemy import Column, Integer, String, func, DateTime, BigInteger, Text, ForeignKey, LargeBinary,\
    UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TournamentTable(Base):
    __tablename__ = 'tournament_table'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), nullable=False)
    team = Column(String, default='')
    game = Column(Integer, default=0)
    victory = Column(Integer, default=0)
    draw = Column(Integer, default=0)
    defeat = Column(Integer, default=0)
    goal = Column(Integer, default=0)
    missed = Column(Integer, default=0)
    difference = Column(Integer, default=0)
    result = Column(Integer, default=0)
    url_team = Column(String)
    logo_team = Column(LargeBinary)
    time_created = Column(DateTime(), server_default=func.now())
    time_updated = Column(DateTime(), onupdate=func.now())

    tournament = relationship('Tournament', back_populates='tournament_tables')

    __table_args__ = (
        UniqueConstraint('team', 'tournament_id'),  # Уникальность по полям team и tournament_id
    )


class Tournament(Base):
    __tablename__ = 'tournament'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    league = Column(String)
    division = Column(String)
    format = Column(String)
    season = Column(String)
    organization = Column(String)
    period = Column(String)
    gender = Column(String, default='М')
    time_created = Column(DateTime(), server_default=func.now())
    time_updated = Column(DateTime(), onupdate=func.now())

    tournament_tables = relationship('TournamentTable', back_populates='tournament')
    players = relationship('Player', back_populates='tournament')


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), nullable=False, index=True)
    game = Column(Integer, default=0)
    goal = Column(Integer, default=0)
    penalty = Column(Integer, default=0)
    assist = Column(Integer, default=0)
    goalpen = Column(Integer, default=0)
    autogoal = Column(Integer, default=0)
    yellowcard = Column(Integer, default=0)
    redcard = Column(Integer, default=0)
    vrt = Column(Integer, default=0)
    prg = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates='players')
    tournament = relationship('Tournament', back_populates='players')

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'tournament_id', 'id'),
        UniqueConstraint('user_id', 'tournament_id')
    )


class Rule(Base):
    __tablename__ = 'rule'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class About(Base):
    __tablename__ = 'about'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class UserPoll(Base):
    __tablename__ = 'user_poll'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    poll_id = Column(BigInteger, ForeignKey('poll.poll_id'), index=True)
    answer = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', backref='users_polls')
    poll = relationship('Poll', backref='users_polls')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    phone = Column(BigInteger, unique=True)
    birthday = Column(String, nullable=False)
    age = Column(Integer)
    role = Column(String, default='')
    avatar = Column(LargeBinary, nullable=True)
    current_club = Column(String, default='Империал')
    previous_clubs = Column(String, default='')
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    players = relationship('Player', back_populates='user', cascade="all, delete")

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'middle_name', 'birthday'),
        # Уникальность по полям first_name и last_name, middle_name, birthday
    )


class Poll(Base):
    __tablename__ = 'poll'
    poll_id = Column(BigInteger, primary_key=True)
    type = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
