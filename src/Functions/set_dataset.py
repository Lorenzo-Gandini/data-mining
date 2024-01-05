import json

# Select the chosen dataset
dataset = 0

def groceries():
    with open("data/pre_processing/json_file/groceries.json","r") as groceries_file:
        groceries = json.load(groceries_file)
    return groceries

def st(dataset):
    with open("data/standard"+str(dataset)+".json","r") as file:
        standard_route = json.load(file)
    return standard_route

def act(dataset):
    with open("data/actual"+str(dataset)+".json","r") as file:
        actual_route = json.load(file)
    return actual_route