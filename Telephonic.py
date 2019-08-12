from telethon import TelegramClient, sync, connection
import socks
import re
from hh_login import api_hash, api_id, pxi_server, pxi_port, pxi_login, pxi_secret

client = TelegramClient('test_kudaibergenov', api_id, api_hash,
                        proxy=(socks.SOCKS5, pxi_server, pxi_port, True, pxi_login, pxi_secret))

client.start()
dialogs = client.get_dialogs()

urls = []
re_pat = re.compile(r'(http|https):\/\/[\da-z-_]+.[a-z]+\/?[\d?=\-_a-zA-Z]')
for message in client.iter_messages(dialogs[0]):
    if not message.text and not message.web_preview:
        continue
    url_str = message.web_preview.url if message.web_preview else message.text
    try:
        match = re.fullmatch(re_pat, url_str)
        if match:
            urls.append(match.group())
            print(match.group())
    except Exception as e:
        print(e)

with open('messages.txt', 'w') as file:
    file.write('\n', join(urls))
