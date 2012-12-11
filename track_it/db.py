from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    String,
    MetaData,
    ForeignKey
)

from sqlalchemy import create_engine
metadata = MetaData()

## define an user table
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('email', String(50)),
    Column('password', String(12))
)

## define a projects table...
## Each task is associated with an project in order to better group tasks

project = Table(
    'projects',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50))
)

## define tasks
## each tasks has a name a description and a time period

tasks = Table(
    'tasks',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('description', Text),
    Column('time_started', Integer),
    Column('time_ended', Integer),
    Column('projects_id', Integer, ForeignKey('projects.id'))
)


def initDB(settings):
    """Create a  engine and build all of the tables"""
    engine = create_engine(settings.get('sqlalchemy'), echo=True)
    metadata.create_all(engine)
