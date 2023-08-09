from calDQ import DQ_VaR, DQ_ES
from optDQ import opt_DQ_VaR, opt_DQ_ES
from dataLoader import dataLoader

import numpy as np 

path = "./data/"
A = dataLoader(path)

print(A.head())
