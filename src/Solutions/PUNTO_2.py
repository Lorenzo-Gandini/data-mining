import json
import Functions.Drivers_rank as Drivers_rank
import Functions.set_dataset as set_dataset

def driver(city_weight, merch_weight,quantity_weight,dataset):

    standard_route = set_dataset.st(dataset)
    actual_route = set_dataset.act(dataset)
    groceries = set_dataset.groceries()

    drivers = []
    for a in actual_route:
        drivers.append(a['driver'])    

    drivers = set(drivers)
    final_list = []
    for id in drivers:
        rank = Drivers_rank.standard_ranked(id,standard_route,actual_route,city_weight, merch_weight,quantity_weight)
        final_list.append(rank)
        print(rank)

    with open("results/driver"+str(dataset)+".json",'w') as outfile:
        json.dump(final_list,outfile,indent = 2)