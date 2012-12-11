from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    Sequence
)

from sqlalchemy import create_engine
metadata = MetaData()
## define an user table

users = Table(
    'users',
    metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('name', String(50)),
    Column('fullname', String(50)),
    Column('password', String(12))
)


def initDB(settings):
    engine = create_engine(settings.get('sqlalchemy'), echo=True)
    metadata.create_all(engine)
