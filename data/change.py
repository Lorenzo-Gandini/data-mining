import json


with open("data/actual9.json",'r') as file:
    act = json.load(file)

'''for a in act:
    if a['driver'] == 'A':
        for trip in a['route']:
            if trip['from'] == 'Verona':
                trip['from'] = 'Bolzano'
            elif trip['to'] == 'Verona':
                trip['to'] = 'Bolzano'

'''
for a in act:
    if a['driver'] == 'A':
        for trip in a['route']:
            if trip['from'] == 'Verona':
                print('Trovato Veronaa')
            elif trip['to'] == 'Verona':
                print('Trovato Veronaa')
                
with open("data/actual9.json",'w') as outfile:
    json.dump(act, outfile, indent = 2)