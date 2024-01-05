import generator as route_generator
import Actual_with_preferences as modify_actual
import copy
import json
import random

with open("data/pre_processing/json_file/groceries.json","r") as file:
    groceries = json.load(file)
with open("data/pre_processing/json_file/cities.json","r") as file:
    cities = json.load(file)

n_dataset = 3
n_standard_routes = 15
step = 10

for i in range (n_dataset):
    n_actual = [0,random.randint(50,200)]

    standard_routes = route_generator.standard_routes_generator(cities,groceries,n_standard_routes)
    n_standard_routes += step
    with open("data/standard"+str(i)+".json",'w') as outfile:
        json.dump(standard_routes, outfile, indent = 2)
        
    actual_tmp = route_generator.actual_routes_generator(standard_routes,n_actual)
    actual_routes = []
    final_route = []

    for route in actual_tmp:
        modified_route = modify_actual.change_city(copy.deepcopy(route), cities, groceries)
        actual_routes.append(modified_route)

    for route in actual_routes:
        modified_route = modify_actual.change_actual(groceries,route['route'])

    with open("data/actual"+str(i)+".json",'w') as outfile:
        json.dump(actual_routes, outfile, indent = 2)