__author__ = 'guillaumemiara'

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from pandas import DataFrame, Series

dataSale = []
dataRent =[]

with open(os.path.join('GarageTemp','garageSale.jsonlines'),'r') as f:
    for line in f:
        dataSale.append(json.loads(line))

with open(os.path.join('GarageTemp','garageRent.jsonlines'),'r') as f:
    for line in f:
        dataRent.append(json.loads(line))

dfsale = DataFrame(dataSale)
print dfsale
dfrent = DataFrame(dataRent)
print dfrent

dfrent.plot(x = 'garage_sale_location' ,y = 'garage_sale_price', kind = 'scatter');
dfsale.plot(x = 'garage_rent_location',y = 'garage_rent_price', kind = 'hexbin', gridsize=25);

plt.show()