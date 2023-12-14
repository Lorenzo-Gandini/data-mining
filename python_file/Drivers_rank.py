import json
import Distance_function 

with open("json_file/standard.json","r") as file:
    standard_route = json.load(file)
with open("json_file/actual.json","r") as file:
    actual_route = json.load(file)

def all_drivers(routes):
    return(routes['driver'])

drivers = []

for a in actual_route:
    drivers.append(all_drivers(a))    

drivers = set(drivers)

def standard_ranked(driver_id,standard_route,actual_route):
    '''
    Function that takes in input a Driver and the standard/actual routes and returns
    a list with the top 5 standard routes for the specific driver ordered from best to worst
    '''
    dizionario_driver = {}

    for act in actual_route:
        if act['driver'] == driver_id:
            for st in standard_route:
                divergence = Distance_function.distance_routes(act,st,0.50,0.35,0.15)
                if st['id'] not in dizionario_driver or divergence < dizionario_driver[st['id']]:
                    dizionario_driver[st['id']] = divergence
                    
    dizionario_driver = dict(sorted(dizionario_driver.items(), key=lambda item: item[1]))

    ranked = {
        "driver" : driver_id,
        "routes" : list(dizionario_driver.keys())[:5]
    }

    return ranked

final_list = []

for id in drivers:
    final_list.append(standard_ranked(id,standard_route,actual_route))
    print(standard_ranked(id,standard_route,actual_route))

with open("json_file/driver.json",'w') as outfile:
    json.dump(final_list,outfile,indent = 2)
