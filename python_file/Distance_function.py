import numpy as np
import json 
import time

def find_min_value(dictionary):
    '''
    Function that returns the key with the lowest value inside the dictionary in input
    '''
    if not dictionary:
        return None, None  # Return None for both key and value if the dictionary is empty

    min_key = min(dictionary, key=dictionary.get)
    min_value = dictionary[min_key]
    
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
    city_shingles_route_1= shingling(route_1)
    city_shingles_route_2= shingling (route_2)
    cummulative_score = 0
    longest_list = city_shingles_route_2
    shortest_list = city_shingles_route_1
    if len(city_shingles_route_1) > len(city_shingles_route_2):
        longest_list = city_shingles_route_1
        shortest_list = city_shingles_route_2
        for index, element in enumerate(longest_list):
            if index < len(shortest_list):
                if element == shortest_list[index]:
                    cummulative_score += 1
                if element != shortest_list[index]:
                    if element in shortest_list:
                        cummulative_score += 0.5
        #1- res per avere la distanza
    if len(set(city_shingles_route_1+city_shingles_route_2))==0:
        return 0
    else:
        return 1- (cummulative_score / len(set(city_shingles_route_1+city_shingles_route_2)))

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

# Compute Hamming distance. Basically it is the number of different bits taken bit-wise.  
def hm_merch(route_1, route_2):
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
    # The decision to return 1 is due to the fact that if the UNION is 0, the distance is MAX
    if union == 0:
        return 1
    # We return distance / union --> because we want all the different measures to be between 0 and 1.
    return distance/union

# Quantity distance. It computes the difference in the quantity of shared products
def qnt_dist(route_1, route_2):
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
        return 0

# Total distance. It computes all the different routes together and put them together to produce the total distance.
# REMEMBER, total DISTANCE, so the lower the better.
def distance_routes(route_1, route_2,city_weight,merch_weight,quantity_weight):
    '''
    Function that takes in input route_1 and route_2 and computes the total distance summing distance_cities,
    distance_products and distance_quantity each one multiplied by a weight.
    '''
    distance_cities = js_city(route_1, route_2)
    distance_products = hm_merch(route_1,route_2)
    distance_quantity = qnt_dist(route_1,route_2)
    distance_total = (distance_cities * city_weight) + (distance_products * merch_weight) + (distance_quantity*quantity_weight)
    #print('id_1: ',route_1['id'],'id_2: ',route_2['id'],'TOTAL DISTANCE: ',distance_total)
    return distance_total

def new_standard(standard_route,actual_routes):
    '''
    Function that takes the standard_route of reference and all the actual_routes 
    '''
    actual_routes.extend([{
        "id": standard_route['id'],
        "route": standard_route['route'],
        "sroute": standard_route['id']
        }])

    id = standard_route['id']

    dist_with_standard = 0
    id_distances_list = []
    id_distances = {}
    
    for i in range(len(actual_routes)):
        if actual_routes[i]['sroute'] == id:
            dis_curr = distance_routes(standard_route,actual_routes[i],0.50,0.35,0.15)
            dist_with_standard += dis_curr
            
            for j in range(i,len(actual_routes)):
                if actual_routes[i]['sroute'] == actual_routes[j]['sroute'] and actual_routes[i]['id'] != actual_routes[j]['id']:
                    
                    id_distances = {
                        (actual_routes[i]['id'],actual_routes[j]['id']) : distance_routes(actual_routes[i], actual_routes[j],0.50,0.35,0.15)
                    }
                    id_distances_list.append(id_distances)
                
                    dis_curr += distance_routes(actual_routes[i], actual_routes[j],0.50,0.35,0.15)
                
    return id_distances_list

start = time.time()

with open("json_file/standard.json","r") as file:
    standard_route = json.load(file)
with open("json_file/actual.json","r") as file:
    actual_route = json.load(file)
with open("pre_processing/json_file/groceries.json","r") as groceries_file:
    groceries = json.load(groceries_file)

new_standard_route = {}

for standard in standard_route:

    id_distances_list = new_standard(standard,actual_route)
    final_distances = {}
    id_list = []

    for actual in actual_route:
        if(standard['id'] == actual['sroute']):
            id_list.append(actual['id'])

    for id_value in id_list:
        result = retrieve_values_by_key(id_distances_list, id_value)
        
        # Calculate the sum of distances for the current ID
        total_distance = sum(result.values())
        
        # Update the final_distances dictionary
        if total_distance > 0:
            final_distances[id_value] = total_distance

        # Print or perform other operations if needed
        min_key,min_value = find_min_value(final_distances)
    #print("Original route :", standard['id'],"New standard route : ",min_key,"Distance :",min_value)

    if min_key != None :
        new_standard_route[standard['id']] = min_key
    else:
        new_standard_route[standard['id']] = standard['id']

output = []

for id,st in enumerate(new_standard_route):
    print(new_standard_route[st])

    for act in actual_route:
        if act["id"] == new_standard_route[st]:
            result_list = [{'id': 's'+str(id), 'route': act['route']}]
            output.append(result_list)
            break

with open("json_file/recStandard.json",'w') as outfile:
    json.dump(output, outfile, indent = 2)

end = time.time()
print(end-start)