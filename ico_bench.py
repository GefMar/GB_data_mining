import os
import shutil
import time
import requests
import random
from itertools import cycle
import settings

site_url = 'https://icobench.com/icos'
params = {"page": 1}
page = 469

if not os.path.exists("html_sources"):
    os.makedirs("html_sources")

os.chdir("html_sources")

for p in range(1, page + 1):
    params["page"] = p
    site_data = requests.get(site_url, params=params)
    if site_data.status_code == 200:
        html_source = site_data.text
        with open("icobench_ico.html", 'w') as file:
            file.write(html_source)
        html_source_file = file.name
        html_source_file_page = "icobench_ico_page_" + str(p) + '.html'
        # shutil.copy(html_source_file, html_source_file_page)
        os.rename(html_source_file, html_source_file_page)
        print("A new HTML source file has been created: ", html_source_file_page)
    else:
        print("The status code is not 200")
    p +=1
    time.sleep(random.randint(1, 5))

os.chdir("..")
