import  Routes_generator as route_generator
import Modify_actual as modify_actual
import copy
import json

with open("pre_processing/json_file/groceries.json","r") as file:
    groceries = json.load(file)

with open("pre_processing/json_file/cities.json","r") as file:
    cities = json.load(file)

n_standard_routes = 5
n_actual = [0,30]

standard_routes = route_generator.standard_routes_generator(cities,groceries,n_standard_routes)

actual_tmp = route_generator.actual_routes_generator(standard_routes,n_actual)
actual_routes = []
final_route = []

for route in actual_tmp:
    modified_route = modify_actual.change_city(copy.deepcopy(route), cities, groceries)
    actual_routes.append(modified_route)

for route in actual_routes:
    modified_route = modify_actual.change_actual(groceries,route['route'])

with open("json_file/actual.json",'w') as outfile:
    json.dump(actual_routes, outfile, indent = 2)
