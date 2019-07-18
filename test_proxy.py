import requests
from itertools import cycle

proxies = ['51.68.95.200:8080',
           '138.197.202.174:3128',
           '94.130.20.85:31288',
           '5.79.227.20:8080']
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'
for i in range(1, 6):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        print("Skipping. Connection error")