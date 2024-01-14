
import Solutions.PUNTO_1 as PUNTO_1
import Solutions.PUNTO_2 as PUNTO_2
import Solutions.PUNTO_3 as PUNTO_3 
from Functions.set_dataset import dataset
city_weight,merch_weight,quantity_weight = 0.55,0.30,0.15

PUNTO_1.recStandard(
    city_weight,merch_weight,quantity_weight,dataset
)
PUNTO_2.driver(
    city_weight,merch_weight,quantity_weight,dataset
)
PUNTO_3.perfectRoutes()

print('Execution completed.\nResults available results/ folder.')