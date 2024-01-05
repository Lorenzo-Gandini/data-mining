# Importing a file containing all the italian counties

import json 

# importing json file
with open('pre_processing/json_file/province-italia.json','r') as province_file:
    province = json.load(province_file)
    
citta = []

for liste in province:  
    citta.append(liste['nome'])

# since we do not need many cities, we keep only the shortest cities for readibility purposes
filtered_cities_list = [item for item in citta if len(item) <= 6]

citta_json = json.dumps(filtered_cities_list)

# save cities in a json file
with open("pre_processing/json_file/cities.json", "w") as outfile:
    outfile.write(citta_json)