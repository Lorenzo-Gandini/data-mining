import time
import Solutions.PUNTO_1 as PUNTO_1
import Solutions.PUNTO_2 as PUNTO_2
import Solutions.PUNTO_3 as PUNTO_3 
from Functions.set_dataset import dataset, act, st
import matplotlib.pyplot as plt
import numpy as np

city_weight,merch_weight,quantity_weight = 0.55,0.30,0.15

"""for i in range(10):
    lista_standard.append(len(st(i)))"""

tempi_merci_nel_ciclo = [19.04080820083618, 50.612844944000244, 84.60229635238647,
                         122.16081404685974, 160.0276918411255, 203.55499958992004,
                         238.76472663879395, 307.64696741104126, 360.80541706085205,
                         359.74274134635925]

tempi_merci_precaricate = [57.67771601676941, 94.77186608314514, 123.91549468040466,
                            159.84641814231873, 195.00686383247375, 224.7241678237915,
                            310.8107087612152, 337.7899875640869, 371.64553928375244,
                            431.7117118835449]

lista_standard = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
act_list = [2, 2, 3, 2, 6, 4, 7, 7, 8, 6]

percentage_list = []

for i in range(len(act_list)):
    percentage_list.append(act_list[i]*100/lista_standard[i])
    print(act_list[i])
    print(lista_standard[i],'\n\n')

# Plotting the bar chart with percentages
plt.bar(lista_standard, percentage_list, width=5, bottom=None, align='center', data=None)

# Adding labels and title
plt.xlabel('Number of Standard Route', fontsize=20)
plt.ylabel('Percentage of New Standards', fontsize=20)
plt.title('New Standard Routes', fontsize=20)

# Show the plot
plt.show()
