import json
import Functions.Distance_function as Distance_function
import Functions.set_dataset as set_dataset

def recStandard(city_weight,merch_weight,quantity_weight,dataset):
    
    standard_route = set_dataset.st(dataset)
    actual_route = set_dataset.act(dataset)

    new_standard_route = {}    
    for standard in standard_route:

        id_distances_list = Distance_function.new_standard(standard,actual_route,city_weight,merch_weight,quantity_weight)
        final_distances = {}
        id_list = []

        for actual in actual_route:
            if(standard['id'] == actual['sroute']):
                id_list.append(actual['id'])

        for id_value in id_list:
            result = Distance_function.retrieve_values_by_key(id_distances_list, id_value)
            # Calculate the sum of distances for the current ID
            total_distance = sum(result.values())
            
            final_distances[id_value] = total_distance
            min_key,min_value = Distance_function.find_min_value(final_distances)
            
                
        new_standard_route[standard['id']] = min_key

        print("Original route :", standard['id'],"New standard route : ",min_key,"Distance :",min_value)
    output = []

    id = 0
    for st in new_standard_route:
        for act in actual_route:
            if act["id"] == new_standard_route[st]:
                if act['route'] not in [item[0]['route'] for item in output]:
                    output.append( [{'id': 's'+str(id), 'route': act['route']}])
                    id+=1
                else : id-=1
                    
    with open("results/recStandard"+str(dataset)+".json",'w') as outfile:
        json.dump(output, outfile, indent = 2)