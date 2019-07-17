import requests
import random
import time
import csv

sate_url = 'https://icobench.com/icos?'
params = {'page':1}
sate_data = requests.get(sate_url, params=params)
time.sleep(random.randint(1, 5))
print (sate_data.url)
data_ICO = sate_data.text
with open(f'data/ICO_bench{params["page"]}.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter =',')
    writer.writerow(data_ICO)
print (data_ICO)