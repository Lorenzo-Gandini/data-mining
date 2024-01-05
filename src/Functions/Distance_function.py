import numpy as np

def find_min_value(final_distances):
    '''
    Function that returns the key with the lowest value inside the input dictionary input
    '''
    min_key = min(final_distances, key=final_distances.get)
    min_value = final_distances[min_key]
    
    return min_key,min_value

def retrieve_values_by_key(id_distances_list, target_value):
    '''
    Function that searches the 'target_value' among the keys in id_distances_list  
    '''
    result = {}

    for dictionary in id_distances_list:
        for key_tuple, value in dictionary.items():
            if any(target_value in element for element in key_tuple):
                # Merge the keys from the tuple into a single key
                merged_key = "-".join(key_tuple)
                result[merged_key] = value
    return result

# Shingling of the routes. It extracts the cities the drivers go through.
def shingling(route):
    '''
    Function to create the set of cities contained in a route
    '''
    route= route['route']
    city_shingles = []
    for i in range(len(route)):
        city_shingles.append(route[i]["from"])
        if i == len(route)-1:
            city_shingles.append(route[i]["to"])
    return city_shingles

# Jaccard similarity of two different routes.
def js_city(route_1, route_2):
    cummulative_score = 0
    city_shingles_route_1 = shingling(route_1)
    city_shingles_route_2 = shingling(route_2)

    if len(city_shingles_route_1)>len(city_shingles_route_2):
        max_len,min_len = len(city_shingles_route_1),len(city_shingles_route_2)
        max_shingle, min_shingle = city_shingles_route_1 , city_shingles_route_2
    else:
        max_len,min_len = len(city_shingles_route_2),len(city_shingles_route_1)
        max_shingle, min_shingle = city_shingles_route_2 , city_shingles_route_1

    # loops through the two shingle's lists
    for i in range(min_len):
        for j in range(max_len):
            if min_shingle[i] == max_shingle[j]:
                # if the values are in the same index +1
                if i == j:
                    cummulative_score += 1
                # if not +0.5
                else:
                    cummulative_score += 0.5

    total_elements = len(set(city_shingles_route_1 + city_shingles_route_2))

    if total_elements == 0:
        return 0

    similarity_score = 1 - (cummulative_score / total_elements)

    return similarity_score

def create_one_hot(route, groceries):
    '''
    Function to create the one hot encoding of the merch carried through the route
    '''
    merch_routes = []
    res = []

    char_to_int = dict((c, i) for i, c in enumerate(groceries))

    for i in range(len(route)):
        merch_routes.append(list(route[i]["merchandise"].keys()))

    for i in merch_routes:
        integer_encoded = [char_to_int[char] for char in i]
        onehot_encoded = list()
        for value in integer_encoded:
            letter = [0 for _ in range(len(groceries))]
            letter[value] = 1
            onehot_encoded.append(letter)

        if onehot_encoded:  # Check if onehot_encoded is not empty
            max_length = max(len(lst) for lst in onehot_encoded)
            padded_lists = [lst + [0] * (max_length - len(lst)) for lst in onehot_encoded]
            res.append([max(bits) for bits in zip(*padded_lists)])

    return res

def merch(route_1, route_2):
    groceries = []
    for route in [route_1, route_2]:
        for route_entry in route['route']:
            if 'merchandise' in route_entry:
                groceries.extend(route_entry['merchandise'].keys())

    groceries = list(set(groceries))
    return groceries
   

# Compute Hamming distance. Basically it is the number of different bits taken bit-wise.  
def hm_merch(route_1, route_2,groceries):
    '''
    Function to compute the Hamming distance (standardized) between route_1 and route_2
    '''
    one_hot_route_1 = create_one_hot(route_1['route'],groceries)
    one_hot_route_2 = create_one_hot(route_2['route'],groceries)
    distance=0
    union=0
    len1, len2 = len(one_hot_route_1), len(one_hot_route_2)

    # Compute Min/Max and difference to then use them in the Hamming Distance 
    min_len = min(len1,len2)
    max_len = max(len1,len2)
    diff_len=max_len- min_len
    
    # .append to the shortest list of the two, to add n list(s) of 0s where n = difference. That makes the two lists the same length   
    if(len1 < len2):
        for i in range(diff_len):
            one_hot_route_1.append([0] * len(groceries))
    elif(len2< len1):
        for i in range(diff_len):
            one_hot_route_2.append([0] * len(groceries))
    for i in range(max_len):
        # union is the number of (unique) items involved in the comparison 
        # distance is the number of times the two routes differ in the merchandise 
        # R1 has milk,oranges - R2 has milk --> union 2 , distance 1
        union += sum(np.bitwise_or(one_hot_route_2[i],one_hot_route_1[i]))
        distance += sum(np.bitwise_xor(one_hot_route_2[i],one_hot_route_1[i]))
    
    # this check is added because otherwise it should divide by 0 --> impossible. 
    # The decision to return 0 is due to the fact that if the UNION is 0, the lists are empty, hence the distance is MIN
    if union == 0:
        return 0
    # We return distance / union --> because we want all the different measures to be between 0 and 1.
    return distance/union

# Quantity distance. It computes the difference in the quantity of shared products
def qnt_dist(route_1, route_2, groceries):
    '''
    Function that computes the quantity distance between route_1 and route_2
    '''
    one_hot_route_2 = create_one_hot(route_2['route'], groceries)
    one_hot_route_1 = create_one_hot(route_1['route'], groceries)
    distance = 0
    sum_values = 0
    len1, len2 = len(one_hot_route_1), len(one_hot_route_2)
    min_len = min(len1, len2)
    int_to_char = dict((i, c) for i, c in enumerate(groceries))
    for i in range(min_len):
        for j in range(len(groceries)):
            if (
                one_hot_route_2[i][j] == 1
                and one_hot_route_1[i][j] == 1
                and int_to_char[j] in route_2['route'][i]["merchandise"]
                and int_to_char[j] in route_1['route'][i]["merchandise"]
            ):
                key = int_to_char[j]
                if route_2['route'][i]["merchandise"][key] >= route_1['route'][i]["merchandise"][key]:
                    sum_values += route_2['route'][i]["merchandise"][key]
                else:
                    sum_values += route_1['route'][i]["merchandise"][key]
                distance += abs(route_2['route'][i]["merchandise"][key] - route_1['route'][i]["merchandise"][key])
    if sum_values != 0:
        return distance / sum_values
    else:
        # Return 1 because sum_values == 0 only when the two trips have no common merchandise.
        return 1

# Total distance. It computes all the different routes together and put them together to produce the total distance.
# REMEMBER, total DISTANCE, so the lower the better.
def distance_routes(route_1, route_2,city_weight,merch_weight,quantity_weight):
    '''
    Function that takes in input route_1 and route_2 and computes the total distance summing distance_cities,
    distance_products and distance_quantity each one multiplied by a weight.
    '''
    # if the two confronted routes are the same routes, distance is automatically 0
    if route_1['id'] == route_2['id']:
        return 0
    distance_cities = js_city(route_1, route_2)
    
    groceries = merch(route_1,route_2)
    distance_products = hm_merch(route_1,route_2,groceries)
    distance_quantity = qnt_dist(route_1,route_2,groceries)
    distance_total = (distance_cities * city_weight) + (distance_products * merch_weight) + (distance_quantity*quantity_weight)
    return distance_total

def new_standard(standard_route,actual_routes,city_weight,merch_weight,quantity_weight):
    '''
    Function that takes the standard_route of reference and all the actual_routes 
    '''
    actual_routes.extend([{
        "id": standard_route['id'],
        "route": standard_route['route'],
        "sroute": standard_route['id']
        }])

    id = standard_route['id']    
    id_distances_list, id_distances = [], {}

    # Loops through the entire list of actual
    for i in range(len(actual_routes)):
        # Picks only the actual based on the given standard  
        if actual_routes[i]['sroute'] == id:
            # Loops from i+1 to avoid calculating the same distance more than once
            for j in range(i+1,len(actual_routes)):
                if actual_routes[i]['sroute'] == actual_routes[j]['sroute'] and actual_routes[i]['id'] != actual_routes[j]['id']:
                    dist = distance_routes(actual_routes[i], actual_routes[j],city_weight,merch_weight,quantity_weight)
                    id_distances = {
                        (actual_routes[i]['id'],actual_routes[j]['id']) : dist
                    }
                    id_distances_list.append(id_distances)
    return id_distances_list