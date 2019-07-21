from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationships

Base = declarative_base()

'''
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id = Column(Integer, unique=True)
    name = Column(String)
    #tmp = relationships('Tmp', backref='product')

    def __init__(self, **kwargs):
        self.s_id = kwargs.get('id')
        self.name = kwargs.get('name')
'''

class ICO(Base):
    __tablename__ = 'ico_info'

    id   							= Column(Integer, primary_key=True, unique=True, autoincrement=True)
    s_id 							= Column(Integer, unique=True)
    name 							= Column(String)
    ticker							= Column(String)
    name_short						= Column(String)
    link							= Column(String)
    logo							= Column(String)
    sto								= Column(Integer)
    goal							= Column(String)
    hype_score_text					= Column(String)
    risk_score_text					= Column(String)
    basic_review_link				= Column(String)
    investment_rating_text			= Column(String)
    investment_rating_link			= Column(String)
    investment_rating_expired		= Column(Boolean)
    investment_rating_tooltip_text	= Column(String)
    investment_rating_end_date		= Column(String)
    raised							= Column(String)
    raised_percent					= Column(String)
    post_ico_end_date				= Column(String)
    post_ico_expired				= Column(Boolean)
    post_ico_tooltip_text			= Column(String)
    post_ico_rating					= Column(String)
    post_ico_rating_status_id		= Column(Integer)
    post_ico_rating_link			= Column(String)
    status							= Column(String)
    tooltip_date					= Column(String)
    tooltip_description				= Column(String)
    can_be_voted					= Column(Boolean)

    def __init__(self, **kwargs):
        self.s_id 							= kwargs.get('id')
        self.name 							= kwargs.get('name')
        self.ticker							= kwargs.get('ticker')
        self.name_short						= kwargs.get('name_short')
        self.link							= kwargs.get('link')
        self.logo							= kwargs.get('logo')
        self.sto							= kwargs.get('sto')
        self.goal							= kwargs.get('goal')
        self.hype_score_text				= kwargs.get('hype_score_text')
        self.risk_score_text				= kwargs.get('risk_score_text')
        self.basic_review_link				= kwargs.get('basic_review_link')
        self.investment_rating_text			= kwargs.get('investment_rating_text')
        self.investment_rating_link			= kwargs.get('investment_rating_link')
        self.investment_rating_expired		= kwargs.get('investment_rating_expired')
        self.investment_rating_tooltip_text	= kwargs.get('investment_rating_tooltip_text')
        self.investment_rating_end_date		= kwargs.get('investment_rating_end_date')
        self.raised							= kwargs.get('raised')
        self.raised_percent					= kwargs.get('raised_percent')
        self.post_ico_end_date				= kwargs.get('post_ico_end_date')
        self.post_ico_expired				= kwargs.get('post_ico_expired')
        self.post_ico_tooltip_text			= kwargs.get('post_ico_tooltip_text')
        self.post_ico_rating				= kwargs.get('post_ico_rating')
        self.post_ico_rating_status_id		= kwargs.get('post_ico_rating_status_id')
        self.post_ico_rating_link			= kwargs.get('post_ico_rating_link')
        self.status							= kwargs.get('status')
        self.tooltip_date					= kwargs.get('tooltip_date')
        self.tooltip_description			= kwargs.get('tooltip_description')
        self.can_be_voted					= kwargs.get('can_be_voted')
