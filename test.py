import csv

text = 'Hello world'
params = {'page':1}
name_file = f'data/ICO_bench{params["page"]}.csv'
with open(f'data/ICO_bench{params["page"]}.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='')
    writer.writerow(text)
