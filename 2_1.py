import requests
url = 'https://icobench.com/icos'

for i in range(1,470):

    print("NEWPAGE=",i)
    param_page = f"page={i}"
    site_data = requests.get(url,params=param_page)
    # print(site_data.status_code)
    my_file = open(f"icobench_ico_page_{i}.html", "w")
    my_file.write(site_data.text)
    my_file.close()