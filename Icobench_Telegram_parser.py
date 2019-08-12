from telethon import TelegramClient, sync, connection
import socks
import re
from login_data import api_hash, api_id, pxi_server, pxi_port, pxi_login, pxi_secret
from pymongo import MongoClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetFullChannelRequest
from time import sleep

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION_ICO = MONGO_DB.icobench
COLLECTION_TG_GROUPS = MONGO_DB.telegram_groups
COLLECTION_TG_USERS = MONGO_DB.telegram_users
re_pat2 = re.compile(r'(http|https):\/\/(t.me|telegram.me)\/[\d?=\-_a-zA-Z\/]*')
re_pat = r'(http|https):\/\/(t.me|telegram.me)\/[\d?=\-_a-zA-Z\/]*'
re_pat3 = re.compile('^(http|https):\/\/(t.me|telegram.me)\/[\d?=\-_a-zA-Z]')

result = COLLECTION_ICO.find({'socials': {'$elemMatch': {'$regex': re_pat2}}}, {'socials': 1, '_id': 0})

tg_list = list(result)

# tg_list2 = []
# for itm in tg_list:
#     tg_list2.append(itm.values())
#
# tg_list3 = list(filter(re_pat2.match, tg_list2))

pre = [i['socials'] for i in tg_list]
links = []
[links.extend(i) for i in pre]
links = [i for i in links if ('t.me' or 'telegram.me') in i]

client = TelegramClient('test_kudaibergenov', api_id, api_hash,
                        proxy=(socks.SOCKS5, pxi_server, pxi_port, True, pxi_login, pxi_secret))

client.start()

print('Beginning parsing Telegram channels')


def parse_channels(tg_channel, client=client):
    try:
        result = client(JoinChannelRequest(tg_channel))
        channel_info = client.get_entity(tg_channel)
        channel_name = channel_info.title
        channel_link = 'https://t.me/' + channel_info.username
        channel_id = channel_info.id

        count = 0
        try:
            for user in client.iter_participants(tg_channel, aggressive=True):
                user_data = user.to_dict()
                find_duplicate = COLLECTION_TG_USERS.find_one({'id': user_data['id']})
                if find_duplicate:
                    _ = COLLECTION_TG_USERS.update_one({'id': user_data['id']}, {"$push": {'channel': channel_name}},
                                                       upsert=False)
                else:
                    user_data['channel'] = channel_name
                    _ = COLLECTION_TG_USERS.insert_one(user_data)
                count += 1
        except Exception as e:
            print(e)
            print('Channel restricts providing user data')

        channel_data = {
            'channel_name': channel_name,
            'ch_id': channel_id,
            'ch_link': channel_link,
            'count': count
        }
        _ = COLLECTION_TG_GROUPS.insert_one(channel_data)

        client(LeaveChannelRequest(tg_channel))
    except Exception as e:
        print(e)
        print('No such channel found')

for item in links:
    channel = str(item)
    print(f'Parsing channel: {channel}')
    parse_channels(item)
    sleep(10)
