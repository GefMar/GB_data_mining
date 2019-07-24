import requests
import time
from alchemy_orm import Icos as DbProduct
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = ' https://icorating.com/ico/all/load/?page=1'

engine = create_engine('sqlite:///icos_rating.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class Icorating:
    icosdata = []

    def __init__(self, url):
        first_page = 1
        # page=0 и page=1 на сайте дублируются, поэтому начинаем с 1.
        last_page = self.get_data(url, 1).get('icos').get('last_page')

        for i in range(first_page, last_page+1):
            time.sleep(1)
            ico_data = self.get_data(url, i)

            for item in ico_data.get('icos').get('data'):
                self.icosdata.append(DbProduct(**item))

            for key, value in ico_data.items():
                setattr(self, key, value)

        session = db_session()
        session.add_all(self.icosdata)

        session.commit()
        session.close()

    def get_data(self, url, i):
        data_site = requests.get(url, params={"page": i})

        return data_site.json()


if __name__ == '__main__':
    collection = Icorating(api_url)
    print('**The End.**')