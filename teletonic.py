from config import api
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
import socks
import re
import json
from pymongo import MongoClient
from time import sleep

CLIENT = MongoClient('192.168.0.202', 27017)
COLLECTION = CLIENT.ico.tg_groups
COLLECTION_USERS = CLIENT.ico.tg_users

proxy = {
    'server': '95.216.224.183',
    'port': 1080,
    'login': '',
    'pass': ''
}

with open('icorating_links.json', 'r') as f:
    icorating_links = json.load(f)

with open('icobench_links.json', 'r') as f:
    icobench_links = json.load(f)


def get_tg_links(data):
    for chat in data:
        name = chat.get('name')
        links = chat.get('socials')
        for link in links:
            if re.findall(r't\.me', link.get('href') if isinstance(link, dict) else link):
                tg_links_icorating.append({'name': name, 'link': link})


tg_links_icorating = []
get_tg_links(icorating_links)
get_tg_links(icobench_links)

client = TelegramClient('gbuhw', api.get('id'), api.get('hash'),
                        proxy=(socks.SOCKS5, proxy['server'], proxy['port'], True))
client.start()

for cur_channel in tg_links_icorating:
    try:
        channel = client.get_entity(cur_channel.get('link'))
        result = client(JoinChannelRequest(channel))
        channel_id = result.chats[0].id
        channel_name = result.chats[0].username
        print(f'process "{channel_name}" channel. ', end="")

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

        print(f'users count: {count}')

        channel_data = {
            'ico_name': cur_channel.get('name'),
            'ch_id': channel_id,
            'ch_name': channel_name,
            'count': count
        }

        _ = COLLECTION.insert_one(channel_data)

        sleep(5)
        client(LeaveChannelRequest(channel))

    except ValueError as e:
        print(f'Username Not Occupied: {cur_channel.get("link")}')
        continue
