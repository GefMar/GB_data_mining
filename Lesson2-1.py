import requests
import time

ico_bench_url = "https://icobench.com/icos"
params = {"page": 1}
file_name_all = "icobench/icobench_ico_page_"

for i in range(1, 470):
    params["page"] = i
    page_data = requests.get(ico_bench_url, params=params)

    file_name = file_name_all + str(params["page"]) + ".html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(page_data.text)
