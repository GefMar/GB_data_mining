from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationships

Base = declarative_base()


class ico_base(Base):
    __tablename__ = 'ICO'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    startup_name = Column(String)
    status = Column(String)
    hype_score = Column(String)    	
    risk_score = Column(String)
    link = Column(String)
    rating = Column(String)
    post_ico = Column(String)
    raised = Column(String)
    raised_procent = Column(String)
    tooltip_date = Column(String)


    #tmp = relationships('Tmp', backref='product')

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.startup_name = kwargs.get('name')
        self.status = kwargs.get('status')
        self.hype_score = kwargs.get('hype_score_text')
        self.risk_score = kwargs.get('risk_score_text')
        self.link = kwargs.get('link')
        self.rating = kwargs.get('post_ico_rating')
        self.post_ico = kwargs.get('post_ico_tooltip_text')
        self.raised = kwargs.get('raised')
        self.raised_procent = kwargs.get('raised_percent')
        self.tooltip_date = kwargs.get('tooltip_date')
        



#class Tmp(Base):
#    pass