import Functions.Distance_function as Distance_function

def standard_ranked(driver_id,standard_route,actual_route,city_weight, merch_weight,quantity_weight):
    '''
    Function that takes in input a Driver and the standard/actual routes and returns
    a list with the top 5 standard routes for the specific driver ordered from best to worst
    '''
    dizionario_driver = {}
    act_driver=[]
    for act in actual_route:
        if act['driver'] == driver_id:
            act_driver.append(act)
            
    for st in standard_route:
        for act in act_driver:
            if st['id'] not in dizionario_driver:
                dizionario_driver[st['id']]= Distance_function.distance_routes(act,st,city_weight, merch_weight,quantity_weight)
            else:
                dizionario_driver[st['id']] += Distance_function.distance_routes(act,st,city_weight, merch_weight,quantity_weight)
    
    dizionario_driver = dict(sorted(dizionario_driver.items(), key=lambda item: item[1]))
    ranked = {
        "driver" : driver_id,
        "routes" : list(dizionario_driver.keys())[:5]
    }
    return ranked