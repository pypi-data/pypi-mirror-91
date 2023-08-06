'''
    Helper Module for fitpy

'''

import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists
from sqlalchemy.orm import sessionmaker

from . import Person
from . import Body
from . import Running

Base = declarative_base()


class FitUser(Base):
    __tablename__ = 'fitpyuser'
    id = Column(Integer, primary_key=True)
    dataset = Column(JSON, nullable=False)


class Database:
    engine = db.create_engine('sqlite:///fitpy.db')
    session = sessionmaker(bind=engine)

    def __init__(self):
        if not database_exists(self.engine.url):
            self.make_database()

    def make_database(self):
        Base.metadata.create_all(self.engine)

    def make_entry(self, data):
        new_entry = FitUser()
        new_entry.id = data[id]
        new_entry.dataset = data

        self.session.add(new_entry)
        self.session.commit()

    def make_query(self, name):
        data = []
        for item in session.query(FitUser).all():
            if name in item:
                data.append(item)
        return data
