from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ICOBase(Base):
    __tablename__ = 'ICO'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    name = Column(String)
    status = Column(String)
    hype_score = Column(String)
    risk_score = Column(String)
    link = Column(String)
    rating = Column(String)
    post_ico = Column(String)
    raised = Column(String)
    raised_percent = Column(String)
    tooltip_date = Column(String)

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.stats = kwargs.get('status')
        self.hype_score = kwargs.get('hype_score_text')
        self.risk_score = kwargs.get('risk_score_text')
        self.link = kwargs.get('link')
        self.rating = kwargs.get('post_ico_rating')
        self.post_ico = kwargs.get('post_ico_tooltip_text')
        self.raised = kwargs.get('raised')
        self.raised_percent = kwargs.get('raised_percent')
        self.tooltip_date = kwargs.get('tooltip_date')
