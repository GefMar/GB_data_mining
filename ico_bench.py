import requests
import random
import time
import csv

sate_url = 'https://icobench.com/icos?'
params = {'page':1}
sate_data = requests.get(sate_url, params=params)
time.sleep(random.randint(1, 5))
print (sate_data.url)
with open('data/wr.csv', 'w') as file:
    writer = csv.writer(file, delimiter ='\n')
    writer.writerow(sate_data)
print (sate_data.text)