from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
import socks
from pymongo import MongoClient
from time import sleep

api_id = 123456
api_hash = 'somesecrethash'

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.telethon
COLLECTION_GROUPS = MONGO_DB.groups
COLLECTION_USERS = MONGO_DB.users
COLLECTION_ICOBENCH = MONGO_DB.icobench
COLLECTION_ICORATING = MONGO_DB.icorating

def get_links(collection):
    links = []
    for record in collection.find():
        for link in record.get('links'):
            if link.find('t.me') > -1:
                links.append((record.get('name'), link))
    return links


telegram_links = get_links(COLLECTION_ICOBENCH)
telegram_links.extend(get_links(COLLECTION_ICORATING))

client = TelegramClient('sessionName1', api_id, api_hash,
                        proxy=(socks.SOCKS5, '154.0.12.233', 8080, True))
client.start()

for link in telegram_links:
    try:
        channel = client.get_entity(link[1])
        result = client(JoinChannelRequest(channel))
        channel_id = result.chats[0].id
        channel_name = result.chats[0].username

        count = 0
        for u in client.iter_participants(channel_name, aggressive=True):
            if u.is_self:
                continue
            result = COLLECTION_USERS.find_one({'id': u.id})
            if result is not None:
                _ = COLLECTION_USERS.update_one({'id': u.id}, {'$push': {'groups': channel_id}})
            else:
                user_info = u.to_dict()
                user_info['groups'] = [channel_id]
                _ = COLLECTION_USERS.insert_one(user_info)
            count += 1

        channel_data = {
            'ico_name': link[0],
            'channel_id': channel_id,
            'channel_name': channel_name,
            'count': count
        }

        _ = COLLECTION_GROUPS.insert_one(channel_data)

        sleep(3)
        client(LeaveChannelRequest(channel))

    except:
        print(f'Error in: {link[0]}: {link[1]}')