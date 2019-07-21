from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Boolean

Base = declarative_base()

class IcoItem(Base):
    __tablename__ = 'icos'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    name = Column(String)
    ticker = Column(String)
    name_short = Column(String)
    link = Column(String)
    logo = Column(String)
    sto = Column(Integer)
    goal = Column(String)
    hype_score_text = Column(String)
    risk_score_text = Column(String)
    basic_review_link = Column(String)
    raised_percent = Column(Float)
    post_ico_expired = Column(Boolean)
    status = Column(String)

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.ticker = kwargs.get('ticker')
        self.name_short = kwargs.get('name_short')
        self.link = kwargs.get('link')
        self.logo = kwargs.get('logo')
        self.sto = kwargs.get('sto')
        self.goal = kwargs.get('goal')
        self.hype_score_text = kwargs.get('hype_score_text')
        self.risk_score_text = kwargs.get('risk_score_text')
        self.basic_review_link = kwargs.get('basic_review_link')
        self.raised_percent = kwargs.get('raised_percent')
        self.post_ico_expired = kwargs.get('post_ico_expired')
        self.status = kwargs.get('status')