import time
import Solutions.PUNTO_1 as PUNTO_1
import Solutions.PUNTO_2 as PUNTO_2
import Solutions.PUNTO_3 as PUNTO_3 
from Functions.set_dataset import dataset, act, st
city_weight,merch_weight,quantity_weight = 0.55,0.30,0.15

begin= time.time()
lista_time=[]
act_list = []
for i in range(1):
    act_list.append(PUNTO_1.recStandard(
        city_weight,merch_weight,quantity_weight,i
    ))
    
    PUNTO_2.driver(
        city_weight,merch_weight,quantity_weight,i
    )
    PUNTO_3.perfectRoutes()
    
    end= time.time()
    # SEARCH FOR 'UPDATE' in the code 

print(act_list)