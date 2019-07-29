from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationships

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    name = Column(String)
    # tmp = relationships('Tmp', backref='product')

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.tmp = kwargs.get('tmp')



class Tmp(Base):
    pass
