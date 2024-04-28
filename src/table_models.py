from db import AbstractBase, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time


class SessionExercises(AbstractBase):
    __tablename__ = 'session_exercises'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    session_id: int = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    exercise_id: int = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    sets: int = Column(Integer, nullable=False)
    reps: int = Column(Integer, nullable=False)

    session = relationship('Sessions', backref='session_exercises')
    exercise = relationship('Exercises', backref='session_exercises')


class Sessions(AbstractBase):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    name: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False)
    time_length: time = Column(Time, nullable=False)
    share_code: int = Column(Integer, nullable=False)

    user = relationship('Users', backref='sessions')


class Exercises(AbstractBase):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    name: str = Column(String, nullable=False)
    muscle_group_id: int = Column(Integer, ForeignKey('muscle_groups.id'), nullable=False)
    photo_name: str = Column(String)
    instructions: str = Column(String, nullable=True)
    
    user = relationship('Users', backref='exercises')
    muscle_group = relationship('MuscleGroups', backref='exercises')


class MuscleGroups(AbstractBase):
    __tablename__ = 'muscle_groups'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name: str = Column(String, unique=True, nullable=False)


class Users(AbstractBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    gender_id: int = Column(Integer, default=1)


class VerificationCodes(AbstractBase):
    __tablename__ = 'verification_codes'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    verification_code: int = Column(Integer, nullable=False)


AbstractBase.metadata.create_all(bind=engine)