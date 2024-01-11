import Functions.Distance_function as Distance_function
from collections import Counter,defaultdict
import Functions.set_dataset as set_dataset 

dataset = set_dataset.dataset
standard_route = set_dataset.st(dataset)
actual_route = set_dataset.act(dataset)
groceries = set_dataset.groceries()

def filter_routes_by_driver(driver_id):
    '''
    Get the routes done by a given driver
    '''
    driver_routes = [route for route in actual_route if route.get('driver') == driver_id]
    return driver_routes

def extract_cities_per_driver(driver_id):
    routes_driver = filter_routes_by_driver(driver_id)
    # UPDATE - removed the function "Generate Basket, because it did the same thing the shingling function does"
    city_pairs = [city for route in routes_driver for city in Distance_function.shingling(route)]
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
    Function that, given a driver, returns how many times he did each standard route
    '''
    routes_driver = filter_routes_by_driver(driver)
    return Counter(route["sroute"] for route in routes_driver)

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
    
def find_cities_standard(driver):
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
    city_driver = extract_cities_per_driver(driver)
    cities_counts = Counter(city_driver)
    frequent_cities_actual = {city: count for city, count in cities_counts.items()}
    cities_to_do = find_cities_standard(driver) 
    
    result_dict = {}
    for key in frequent_cities_actual:
        result_dict[key] = (frequent_cities_actual[key] - cities_to_do.get(key, 0)) + (frequent_cities_actual[key] / 2)
    
    n = calculate_avg_route_length_driver(driver)
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



def merchandise_standard_cities(s_counter):
    '''
    Function that returns a list of all the cities the driver had to visit and how many times
    he should have brought each item to that city
    '''
    city_counts = defaultdict(lambda: defaultdict(int))

    for s, count in s_counter.items():
        for route in standard_route:
            if route['id'] == s:
                for i in range(len(route['route'])):
                    city = route['route'][i]['to']
                    merchandise_list = list(route['route'][i]['merchandise'].keys())

                    for item in merchandise_list:
                        city_counts[city][item] += count
                        
    standard_merch = {k: v for city, items in city_counts.items() for k, v in {city: dict(items)}.items()}
    return standard_merch 

def merchandise_actual_cities(driver):
    result = {}
    merch_city = {}

    for route_info in actual_route:
        if route_info['driver'] != driver:
            continue
        route = route_info['route']

        for leg in route:
            destination = leg['to']
            merchandise = leg['merchandise']

            if destination not in merch_city:
                merch_city[destination] = {}

            for item, quantity in merchandise.items():
                if item not in merch_city[destination]:
                    merch_city[destination][item] = 1
                else:
                    merch_city[destination][item] += 1
                    
    for destination, items in merch_city.items():
        merch_city[destination] = dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

    result[driver] = merch_city

    return result


def calculate_difference_actual_standard(actual_merch, standard_merch):
    result_dict = {}

    for city, items_dict2 in standard_merch.items():
        result_dict[city] = {}
        for item, count_st in items_dict2.items():
            count_act = actual_merch.get(city, {}).get(item, 0)
            if count_act != 0:
                result_dict[city][item] = (count_act - count_st) + count_act / 2
    for city, items_dict1 in actual_merch.items():
        if city not in result_dict:
            result_dict[city] = {}

        for item, count_act in items_dict1.items():
            if item not in result_dict[city]:
                result_dict[city][item] = (count_act) + count_act / 2
    return result_dict



def get_top_items_per_city(relevant_merch, driver,driver_habits):
    '''
    Function that returns the top n items, where n is the average number of products carried during a trip  
    '''
    top_items = {}
    for city, items in relevant_merch.items():
        top_items[city]={}
        if items is not None:
            n = driver_habits[driver][city]
            top_items[city] = dict(sorted(items.items(), key=lambda x: x[1], reverse=True)[:n])
    return top_items

def get_top_items_by_city_and_quantity(dict, driver):
    for city, items in dict.items():
        for key in items:
            dict[city][key]= average_quantity_of_product(driver, city, key)
    return dict

def average_quantity_of_product(driver,city,product):
    total_quantity = 0
    total_routes = 0

    for route_info in actual_route:
        if route_info['driver'] == driver:
            route = route_info['route']
            for leg in route:
                merchandise = leg.get('merchandise', {})
                destination = leg['to']
                if product in merchandise and city==destination:
                    total_quantity += merchandise[product]
                    total_routes += 1
    if total_routes == 0:
        return 0  # Avoid division by zero if the product is not found in any route

    average_quantity = round(total_quantity / total_routes- 0.5) + 1
    return average_quantity

# UPDATE
def avg_n_product_per_city(driver):
    '''
    Function that returns how many (different) merchandise products he carries to each city on average.
    '''
    driver_merch = {}
    delivery = []
    for actual in actual_route:
        if actual['driver'] == driver:
            for route in actual['route']:
                city = route['to']
                delivery.append([city,len(route['merchandise'])])
        driver_merch[driver] = delivery
    collapsed_dict = {}
    for letter, city_data in driver_merch.items():
        city_sum = {}
        city_count = {}
        for city, value in city_data:
            if city in city_sum:
                city_sum[city] += value
                city_count[city] += 1
            else:
                city_sum[city] = value
                city_count[city] = 1

        collapsed_dict[letter] = {
            city: round(city_sum[city] / city_count[city]) for city in city_sum
        }
    return collapsed_dict

def analyze_driver_data(driver):
    # UPDATE
    n_product_per_city = avg_n_product_per_city(driver)
    actual_merch = merchandise_actual_cities(driver)
    s_counter = count_standard_routes(driver)
    standard_merch = merchandise_standard_cities(s_counter)
    top_merch = calculate_difference_actual_standard(actual_merch[driver], standard_merch)
    top_cities_driver = find_favorite_cities(driver)
    relevant_merch = {key: top_merch.get(key, None) for key, _ in top_cities_driver}
    top_items_by_city = get_top_items_per_city(relevant_merch, driver,n_product_per_city)
    top_items_by_city_and_quantity= get_top_items_by_city_and_quantity(top_items_by_city,driver)

    return top_items_by_city_and_quantity