import random

# Create a function that slightly modifies the previous routes


def change_city(route, cities, groceries):
    '''
    Function that takes a city1 in the input route and it substitutes it with a city1 from 
    the available cities (taken from the cities.json) not currently present in the route
    n_trips is the number of trips the route is composed of
    '''
    n_trips = len(route['route'])

    n_changes = random.randint(0,n_trips)

    for i in range(n_changes):
        n_trips = len(route['route'])

        operation = random.randint(0,2)
        # 0 change , 1 remove , 2  add

        idx = random.randint(0,n_trips)

        if operation == 0:
            idx = random.randint(0,n_trips)
            
            # if the idx is the starting point
            if idx == 0:
                city1 = random.choice(cities) 
                while city1 ==  route['route'][idx]['to']:
                    city1 = random.choice(cities) 
                
                route['route'][idx]['from'] = city1
            
            elif idx == n_trips:
                # if idx is the destination
                city1 = random.choice(cities) 
                while city1 ==  route['route'][idx-1]['from']:
                    city1 = random.choice(cities) 
                
                route['route'][idx-1]['to'] = city1
            
            else: 
                city1 = random.choice(cities)
                while city1 == route['route'][idx-1]['from'] or city1 == route['route'][idx]['to']:
                    city1 = random.choice(cities)
            
                route['route'][idx-1]['to'] = city1
                route['route'][idx]['from'] = city1

        elif operation == 1:
             # if the idx is the starting point
            if idx == 0:
                route['route'].pop(idx)

            # if the idx is the destination
            elif idx == n_trips:
                route['route'].pop(idx-1)

            # if the idx is a random city along the route['route']
            else :
                route['route'][idx-1]['to'] = route['route'][idx]['to']
                route['route'].pop(idx)

        elif operation == 2:
            # if the idx is the starting point
            if idx == 0:
                city1 = random.choice(cities) 
                while city1 ==  route['route'][idx]['from']:
                    city1 = random.choice(cities) 
            
                city2 = route['route'][idx]['from']

            # if the idx is the destination
            elif idx == n_trips:
                city2 = random.choice(cities) 
                while city2 ==  route['route'][idx-1]['to']:
                    city2 = random.choice(cities) 
            
                city1 = route['route'][idx-1]['to']

            # if the idx is a random city along the route
            else :
                city1 = random.choice(cities) 
                while city1 ==  route['route'][idx-1]['from']:
                    city1 = random.choice(cities) 
            
                city2 = route['route'][idx-1]['to']
                route['route'][idx-1]['to'] = city1

            unique_groceries = random.sample(groceries, random.randint(1,5))
                
            # Initializing the dictionary where the merchandise will be store in.
            # Generating the quantity for every item.
            item_qnt = {grocery: random.randint(1, 50) for grocery in unique_groceries}

            # Generating the different trips with the merchandise carried.
            dict = {
                "from" : city1,
                "to" : city2,  
                "merchandise" : item_qnt
            }
            
            route['route'].insert(idx,dict)
    
    return route

def change_actual(groceries,routes):
    '''
    Function that takes in input a single route and change the quantity of items carried
    '''
    for route in routes:
        dict_append = {}
        list_remove = []

        # Create a list of keys to remove or modify
        keys_to_modify = list(route['merchandise'].keys())

        for key in keys_to_modify:
            item = route['merchandise'][key]
            case = random.randint(0, 4)

            if case == 1:
                # change item
                merch = list(route['merchandise'].keys())
                available_strings = list(set(groceries) - set(merch))
                new_merch = random.choice(available_strings)
                dict_append[new_merch] = route['merchandise'].pop(key)

            elif case == 2:
                # change qnt
                route['merchandise'][key] = random.randint(1, 50)

            elif case == 3:
                # remove
                list_remove.append(key)

            elif case == 4:
                # add item
                merch = list(route['merchandise'].keys())
                available_strings = list(set(groceries) - set(merch))
                new_merch = random.choice(available_strings)
                dict_append[new_merch] = random.randint(1, 50)

        # Remove items outside the loop
        for remove in list_remove:
            route['merchandise'].pop(remove)

        # Update the dictionary outside the loop
        route['merchandise'].update(dict_append)