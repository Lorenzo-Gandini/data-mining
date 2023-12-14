import json
from collections import Counter
from collections import defaultdict

def convert_to_standard_structure(actual_merch):
    standard_merch = {}

    for category, locations in actual_merch.items():
        if category not in standard_merch:
            standard_merch[category] = {}

        for location, items in locations.items():
            if location not in standard_merch[category]:
                standard_merch[category][location] = {}

            for item, quantity in items:
                if item not in standard_merch[category][location]:
                    standard_merch[category][location][item] = quantity
                else:
                    standard_merch[category][location][item] += quantity

    return standard_merch

def filter_routes_by_driver(driver_id):
    '''
    Get the routes done by a given driver
    '''
    driver_routes = [route for route in actual_route if route.get('driver') == driver_id]
    return driver_routes

def generate_basket(driver_route):
    route = driver_route['route']
    basket = []
    for i in range(len(route)):
        basket.append(route[i]["from"])
        if i == len(route)-1:
            basket.append(route[i]["to"])
    return basket

def extract_cities_per_driver(driver_id):
    '''
    Extract cities from each route
    '''
    routes_driver = filter_routes_by_driver(driver_id)
    city_pairs = []
    for i in routes_driver:
        city_pairs += generate_basket(i)

    return city_pairs

def calculate_avg_route_length_driver(driver):
    '''
    Function that returns the average length of all the routes done by a given driver
    '''
    routes_driver = filter_routes_by_driver(driver)
    counter = 0
    for route in routes_driver:
        leng = len(route["route"])
        counter += leng
    return int(counter/len(routes_driver))

def count_standard_routes(driver):
    '''
    Function that counts how many times each standard route is done by a given driver
    '''
    standard_counter_dict = {}
    routes_driver = filter_routes_by_driver(driver)
  
    for route in routes_driver:
        if route["sroute"] not in standard_counter_dict:
            standard_counter_dict[route["sroute"]] = 1
        else:
            standard_counter_dict[route["sroute"]] += 1
    return standard_counter_dict

def create_standard_cities_dict(one_standard_route, value):
    cities_dict = {}
    for st in standard_route:
        if st["id"] == one_standard_route:
            route = st['route']
            for i in range(len(route)):
                if route[i]['from'] in cities_dict:
                    cities_dict[route[i]["from"]] += 1
                else:
                    cities_dict[route[i]["from"]] = value
                if i == len(route)-1:
                    if route[i]['to'] not in cities_dict:
                        cities_dict[route[i]["to"]] = value

    return cities_dict
    
def find_routes_frequency(driver):
    '''
    Creates a dictionary that counts how many times a standard route is done by a given driver
    '''
    final_dict = {}
    counter_standard = count_standard_routes(driver)
    for key, value in counter_standard.items():
        dict_curr = create_standard_cities_dict(key, value)
        for key, value in dict_curr.items():
            if key in final_dict:
                final_dict[key] += value
            else:
                final_dict[key] = value
    return final_dict
  
def find_favorite_cities(driver):
    '''
    Finds the driver's favorite cities.
    It finds how many times the driver goes to a certain city and how many times he was supposed to go there and he subtracts the two.
    A positive number indicates that the driver went to a city more times than he was supposed to, so we assume he likes the city. On the 
    contrary, if the number is negative, it means the driver avoided the city.
    '''
    city_driver_e = extract_cities_per_driver(driver)

    pair_counts = Counter(city_driver_e)

    frequent_cities_actual = {pair: count for pair, count in pair_counts.items()}
    cities_to_do = find_routes_frequency(driver)  
    n = calculate_avg_route_length_driver(driver)

    result_dict = {key: frequent_cities_actual[key] - cities_to_do.get(key, 0) for key in frequent_cities_actual}
    result_dict_ordered = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)[:n]    

    return result_dict_ordered

def get_drivers_from_routes():
    '''
    Function that extracts the drivers from the routes.
    '''
    drivers_list = []
    for route in actual_route:
      drivers_list.append(route['driver'])

    return set(drivers_list)

def standard_merchandise(standard_route):
    stand_mer = {}

    for route in standard_route:
        dix = {}
        
        for trip in route['route']:
            dest = trip['to']
            merch_count = Counter()

            for item, count in trip['merchandise'].items():
                merch_count[item] += 1
            # Convert Counter to dictionary
            merch_count_dict = dict(merch_count)

            if dest not in dix:
                dix[dest] = merch_count_dict
            else:
                dix[dest] = {k: dix[dest].get(k, 0) + v for k, v in merch_count_dict.items()}

        stand_mer[route['id']] = dix

    return stand_mer

def merchandise_standard_cities(s_counter):
    '''
    Function that takes the actual routes and the driver. It returns a list of all the cities the driver has been to and how many times
    he took each item to that city
    '''
    lista_merci = []

    for s, count in s_counter.items():
        dix = {}  # Initialize the dictionary outside the loop

        for route in standard_route:
            if route['id'] == s:
                for i in range(len(route['route'])):
                    city = route['route'][i]['to']
                    merchandise_list = list(route['route'][i]['merchandise'].keys())

                    if city not in dix:
                        dix[city] = {}

                    for item in merchandise_list:
                        # Multiply the merchandise count by the corresponding value in s_counter
                        multiplied_count = route['route'][i]['merchandise'][item] = count

                        # Update the count in the dictionary
                        if item not in dix[city]:
                            dix[city][item] = multiplied_count
                        else:
                            dix[city][item] += multiplied_count

        lista_merci.append({s: dix})

    lista_merci = collapse_city_counts(lista_merci)

    return lista_merci

def collapse_city_counts(merchandise_list):
    city_counts = defaultdict(lambda: defaultdict(int))

    for entry in merchandise_list:
        for key, value in entry.items():
            for city, items in value.items():
                for item, count in items.items():
                    city_counts[city][item] += count

    result = [{city: dict(items)} for city, items in city_counts.items()]
    return result  

def merchandise_actual_cities(driver):
    '''
    Function that takes the actual routes and the driver. It returns a list of all the cities the driver has been to and how many times
    he took each item to that city
    '''
    merch_city = {}
    quantity_merch = {}

    for route_info in actual_route:
        if route_info['driver'] != driver:
            continue
        route = route_info['route']

        for leg in route:
            destination = leg['to']
            merchandise = leg['merchandise']

            for item, quantity in merchandise.items():
                if destination not in merch_city:
                    merch_city[destination] = {}
                    quantity_merch[destination] = {}

                # If it is the first time the given product appears in the given city
                if item not in merch_city[destination]:
                    merch_city[destination][item] = 1
                    quantity_merch[destination][item] = quantity

                else:
                    merch_city[destination][item] += 1
                    quantity_merch[destination][item] += quantity
                
                quantity_merch[destination][item] = quantity_merch[destination][item] / merch_city[destination][item]
                quantity_merch[destination][item] = round(quantity_merch[destination][item] - 0.5) + 1

    for destination, items in merch_city.items():
        merch_city[destination] = (sorted(items.items(), key=lambda x: x[1], reverse=True))

    return merch_city, quantity_merch

def calculate_difference_actual_standard(actual_merch, standard_merch):
    '''
    Once we have the two different dictionaries (for items in the actual and items in the standard) we use this function 
    to find the favorite items to carry in the different cities.
    Results from : - inf to + inf --> high score means the driver likes the item. 
    '''
    result_dict = {}

    for city, items_dict2 in standard_merch.items():
        result_dict[city] = {}
        for item, quantity2 in items_dict2.items():
            quantity1 = actual_merch.get(city, {}).get(item, 0)
            if(quantity1 != 0):
                result_dict[city][item] = quantity1 - quantity2

    # Include cities that are in actual_merch but not in standard_merch
    for city, items_dict1 in actual_merch.items():
        if city not in result_dict:
            result_dict[city] = {}
        for item, quantity1 in items_dict1.items():
            if item not in result_dict[city]:
                result_dict[city][item] = quantity1

    return result_dict

def calculate_avg_products_per_route_driver(driver):
    '''
    Function that returns the average length of all the routes done by a given driver
    '''
    routes_driver = filter_routes_by_driver(driver)
    counter = 0
    sum_len_route = 0
    for route in routes_driver:
        sum_len_route += len(route["route"])
        for merch in route["route"]:
            counter += len(merch['merchandise'])

    return int(counter/sum_len_route)

def get_top_items_per_city(relevant_merch, driver):
    '''
    Function that returns the top n items, where n is the average number of products carried during a trip  
    '''
    top_items = {}
    for city, items in relevant_merch.items():
        # Check if items is not None before processing
        if items is not None:
            top_items[city] = dict(sorted(items.items(), key=lambda x: x[1], reverse=True)[:calculate_avg_products_per_route_driver(driver)])
        else:
            # Case where items is None
            top_items[city] = {} 

    return top_items

def analyze_driver_data(driver):
    actual_merch, quantity_merch = merchandise_actual_cities(driver)
    s_counter = count_standard_routes(driver)
    supposed_merch = merchandise_standard_cities(s_counter)
    standard_merch = {k: v for data_dict in supposed_merch for k, v in data_dict.items()}
    actual_merch = convert_to_standard_structure({driver: actual_merch})

    top_merch = calculate_difference_actual_standard(actual_merch[driver], standard_merch)

    top_cities_driver = find_favorite_cities(driver)

    relevant_merch = {key: top_merch.get(key, None) for key, _ in top_cities_driver}

    top_items_by_city = get_top_items_per_city(relevant_merch, driver)

    for key, value in top_items_by_city.items():
        for sub_key, sub_value in value.items():
            if key in quantity_merch and sub_key in quantity_merch[key]:
                top_items_by_city[key][sub_key] = quantity_merch[key][sub_key] 

    return top_items_by_city


with open("json_file/standard.json", "r") as file:
    standard_route = json.load(file)
with open("json_file/actual.json", "r") as file:
    actual_route = json.load(file)

# Get the list of drivers
drivers = get_drivers_from_routes()

final_driver = {}

for driver in drivers:
    final_driver[driver] = analyze_driver_data(driver)


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

# Convert the data to JSON
json_output = json.dumps(output_data, indent=2)
print(json_output)

with open("json_file/perfectRoute.json",'w') as outfile:
    json.dump(output_data, outfile, indent = 2)