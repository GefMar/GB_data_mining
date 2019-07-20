from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationships

Base = declarative_base()


class ico_base(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    startup_name = Column(String)
    status = Column(String)
    hype_score = Column(String)    	
    risk_score = Column(String)
    basic_Review = Column(String)
    rating = Column(String)
    post_ico = Column(String)
    raised = Column(String)
    raised_procent = Column(String)



    tmp = relationships('Tmp', backref='product')

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.name = kwargs.get('name')


class Tmp(Base):
    pass