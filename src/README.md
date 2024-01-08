# Data Mining a.y. 2023-2024
Repository for the Data Mining project course
Simonato Nicolò - Russo Riccardo - Gandini Lorenzo

To run the program, follow these steps:

1) If you want to change the standard and actual routes, insert the new routes in the "/data" folder with the correct format (standardX.json / actualX.json) where X is an integer. You can also use the existing ones.

2) In "src/Functions/set_dataset.py," set the variable "dataset" to the desired dataset number (X).

3) OPTIONAL: In the src/Main.py script, there are three variables: city_weight, merch_weight, quantity_weight. They represent the importance assigned to passing through cities in the standard routes, the importance of delivering predefined products, and the quantity to be delivered, respectively. These weights are pre-set to 55%, 30%, and 15% (These weights alterate the result in the distance function). However, they can be changed based on user preferences.

4) Run "src/Main.py".

5) The results will be stored in 'results/'. With names :
    For point 1 --> results/recStandardX.json
    For point 2 --> results/driverX.json
    For point 3 --> results/perfectRouteX.json
