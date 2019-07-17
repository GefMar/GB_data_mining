import requests
import random
import time

sate_url = 'https://icobench.com/icos?'
params = {'page':1}
while params["page"]<469:    
    params["page"] += 1
    print (params["page"]) 