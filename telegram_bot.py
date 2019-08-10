from telethon import TelegramClient, sync
from telethon.errors import InviteHashExpiredError, UsernameNotOccupiedError
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
import socks
from pymongo import MongoClient

mongo = MongoClient('', 27017)
db = mongo.icodb
db.drop_collection('telegram_channels')
db.drop_collection('telegram_members')

api_hash = ''
api_id = 0

proxy_server = ''
proxy_port = 0
proxy_login = ''
proxy_pass = ''

client = TelegramClient('tele_session', api_id, api_hash,
                        proxy=(socks.HTTP, proxy_server, proxy_port, False, proxy_login, proxy_pass)).start()

icorating = db.icorating.find()
channels = {}
people = {}

# Populate channels with entities
for ico in icorating:
    if len(channels) > 1:
        break
    for link in ico['links']:
        if ('t.me' or 'telegram') in link:
            try:
                channels.update({
                    link: {
                        'channel_id': 0,
                        'link': link,
                        'entity': client.get_entity(link),
                        'title': '',
                        'count': 0}
                    })
            except (InviteHashExpiredError, UsernameNotOccupiedError, ValueError):
                print('{} expired'.format(link))

print('begin')
# Complete channelsinfo and populate people dict
for (k, v) in channels.items():
    client(JoinChannelRequest(v['entity']))
    dialogs = client.get_dialogs()
    participants = client.get_participants(dialogs[0])
    channels[k]['channel_id'] = dialogs[0].entity.id
    channels[k]['title'] = dialogs[0].title
    channels[k]['count'] = participants.total
    for itm in participants:
        # Just add new channel if user exists
        if people.get(itm.id, None):
            people[itm.id]['channels'].append(dialogs[0].entity.id)
            print('User with many channels!', people[itm.id])
        # Or add new user to dict
        else:
            people.update({
                itm.id: {
                    'username': itm.username,
                    'first_name': itm.first_name,
                    'last_name': itm.last_name,
                    'channels': [dialogs[0].entity.id]}
            })
    client(LeaveChannelRequest(v['entity']))
    channels[k].pop('entity')
    db['telegram_channels'].insert_one(channels[k])

# Prepare people to insert
people_to_insert = [{
    'user_id': k,
    'username': v['username'],
    'first_name': v['first_name'],
    'last_name': v['last_name'],
    'channels': v['channels']} for (k, v) in people.items()]
db['telegram_members'].insert_many(people_to_insert)

print('end')
