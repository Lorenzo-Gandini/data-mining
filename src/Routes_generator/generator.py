# Python script to generate the different routes. It returns two different JSON Files called 
# "actual.json" and "standard.json"
import random
import string
import json

def standard_routes_generator(cities,groceries,n_standard_routes):
    '''
    Function that takes in input 2 lists: 1 list of cities and 1 list of groceries and 1 the number of routes
    '''
    routes = []
    # Number of total ROUTES.
    for i in range(n_standard_routes):
        
    # Shuffling the different lists to ensure the creation of different trips/routes.
        random.shuffle(cities)
        random.shuffle(groceries)

        unique_groceries = ''

        # This list is declared inside the first For-loop to "empty it" at every iteration.
        list_cities = []

        # n_trips is the number of trips in a route. 
        # It is between 2 and n 
        n_trips = random.randint(2,10)

        # Number of total TRIPS 
        for j in range(n_trips):
            # Create a sample of 3 distinct items.
            unique_groceries = random.sample(groceries, (random.randint(1,10)))
            
            # Initializing the dictionary where the merchandise will be store in.
            # Generating the quantity for every item.
            item_qnt = {grocery: random.randint(1, 50) for grocery in unique_groceries}

            # Generating the different trips with the merchandise carried.
            dict = {
                "from" : cities[j-1],
                "to" : cities[j],  
                "merchandise" : item_qnt
            }
            list_cities.append(dict)

        # A temporary dictionary needed to pair the routes with their id.
        route_tmp = {
            "id" : 's' + str(i),
            "route" : list_cities,
        }
        routes.append(route_tmp)

    return routes

def actual_routes_generator(routes,boundaries):
    '''
    Function that takes the standard routes and duplicate each standard a random number of times.
    '''
    start_letter = "A"
    end_letter = "E"
    actual_routes = []
    actual_id = 0

    for route in routes:
        # n_actual is the number of actual generated for every single standard route
        # boundaries is the variable passed by input from the main to make things quicker.
        n_actual = random.randint(boundaries[0],boundaries[1])
        for j in range(n_actual):
                
            # Adding the "driver" key and value to each route
            dict_act = {
                "id": "a"+str(actual_id),
                "driver": random.choice(string.ascii_uppercase[string.ascii_uppercase.index(start_letter):string.ascii_uppercase.index(end_letter) + 1]), 
                "sroute" : route["id"],
                "route": route["route"]
            }

            actual_routes.append(dict_act)
            actual_id+=1

    return actual_routes