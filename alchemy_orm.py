from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationships


Base = declarative_base()


class Ico(Base):
    __tablename__ = 'icos'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    ext_id = Column(Integer, unique=True)
    name = Column(String)
    # rel = relationships('Rel', backref='icos')

    def __init__(self, **kwargs):
        self.ext_id = kwargs.get('id')
        self.name = kwargs.get('name')


class Rel(Base):
    pass
