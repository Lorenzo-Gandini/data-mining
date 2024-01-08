import Functions.Perfect_routes as Perfect_routes
import json
from Functions.set_dataset import dataset

def perfectRoutes():

    drivers = Perfect_routes.get_drivers_from_routes()

    final_driver = {}
    for driver in drivers:
        final_driver[driver] = Perfect_routes.analyze_driver_data(driver)

    output_data = []
    for driver, routes in final_driver.items():
        route_list = []
        from_cities = list(routes.keys())
        for i in range(len(from_cities) - 1):
            from_city = from_cities[i]
            to_city = from_cities[i + 1]
            merchandise = routes[to_city]
            
            route = {
                'from': from_city,
                'to': to_city,
                'merchandise': merchandise
            }
            route_list.append(route)

        output_data.append({'driver': driver, 'route': route_list})
        
    with open("results/perfectRoute"+str(dataset)+".json",'w') as outfile:
        json.dump(output_data, outfile, indent = 2)

    #print(final_driver)