# Importing a file containing the 100 most popular items

import json

# importing json file
with open('pre_processing/json_file/products.json','r') as file_prodotti:
    spesa = json.load(file_prodotti)

prodotti = []

for lista in spesa:
    prodotti.append(lista['title'])

# since we do not need many cities, we keep only the shortest groceries for readibility purposes
filtered_products_list = [item for item in prodotti if len(item) <= 8]

products_json = json.dumps(filtered_products_list)

# save cities in a json file
with open("pre_processing/json_file/groceries.json", "w") as outfile:
    outfile.write(products_json)