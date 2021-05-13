import requests
from alchemy_orm import Base
from alchemy_orm import Ico as DbIco
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import session
from sqlalchemy import create_engine


icorating_api_url = 'https://icorating.com/ico/all/load/?page=1'

engine = create_engine('sqlite:///icorating.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class Icorating:
    icos = []
    next = None
    previous = None

    def __init__(self, url):

        while True:
            if self.next:
                data = self.get_next_data(self.next)
            else:
                data = self.get_next_data(url)

            for item in data.get('results'):
                self.icos.append(DbIco(**item))

            for key, value in data.items():
                setattr(self, key, value)

            if not data['next']:
                break

        session = db_session()
        session.add_all(self.icos)

        session.commit()
        session.close()

    def get_next_data(self, url):
        return requests.get(url).json()


class Ico:
    def __init__(self, ico_dict):
        for key, value in ico_dict.items():
            setattr(self, key, value)


if __name__ == '__main__':
    collection = Icorating(icorating_api_url)
    print('***')
