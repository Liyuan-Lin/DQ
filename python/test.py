from calDQ import DQ_VaR, DQ_ES
from optDQ import opt_DQ_VaR, opt_DQ_ES
from dataLoader import dataLoader

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path = "./data/"

alpha = 0.1


n_training = 500

loss_ratio = pd.read_excel("./test/test_data.xlsx", index_col=False, header=None)


n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  


w = np.ones(n_stock) / n_stock


DQVaR = DQ_VaR(alpha, loss_ratio.values)

DQES = DQ_ES(alpha, loss_ratio.values)

# calculate the optimal investment weight that minimizes the DQ_VaR
w, _ = opt_DQ_VaR(alpha, loss_ratio.values, tie_breaker=True, w_0=w)

v, _ = opt_DQ_ES(alpha, loss_ratio.values, tie_breaker=True, w_0=w)

print(DQVaR)

print(DQES)

print(w)

print(v)

