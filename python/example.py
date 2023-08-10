from calDQ import DQ_VaR, DQ_ES
from optDQ import opt_DQ_VaR, opt_DQ_ES
from dataLoader import dataLoader

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path = "./data/"

alpha = 0.05



n_training = 500

loss_ratio = dataLoader(path, start_date="2011-01-01")

n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  

start_year, start_month = 2014, 1
end_year, end_month = 2021, 12

initial_value = 1000
opt_w_DQVaR= {}
opt_w_DQES= {}
w = np.ones(n_stock) / n_stock

for year in range(start_year, end_year + 1):

    for month in range(1, 13):

        current_date = str(year) + "-" + str(month).zfill(2) + "-00"

        training_data = loss_ratio.loc[:current_date][-n_training:]

        # calculate the optimal investment weight that minimizes the DQ_VaR
        w, _ = opt_DQ_VaR(alpha, training_data.T.values, tie_breaker=True, w_0=w)
    
        opt_w_DQVaR[loss_ratio.loc[current_date:].index[0]] = w

        v, _ = opt_DQ_ES(alpha, training_data.T.values, tie_breaker=True, w_0=w)

        opt_w_DQES[loss_ratio.loc[current_date:].index[0]] = v


# put optimal weight into a dataframe
opt_w_DQVaR = pd.DataFrame(opt_w_DQVaR, index=loss_ratio.columns).T

opt_w_DQES = pd.DataFrame(opt_w_DQES, index=loss_ratio.columns).T

loss_ratio.index = pd.to_datetime(loss_ratio.index)

# calculate the monthly return 
return_M = (1-loss_ratio).resample("M").prod().loc["2014-01-01":]

return_M.index = opt_w_DQVaR.index

portfolio_value_DQVaR = (return_M * opt_w_DQVaR).sum(axis=1).cumprod(axis=0) * initial_value

portfolio_value_DQVaR.index = pd.to_datetime(portfolio_value_DQVaR.index)

portfolio_value_DQES = (return_M * opt_w_DQES).sum(axis=1).cumprod(axis=0) * initial_value

portfolio_value_DQES.index = pd.to_datetime(portfolio_value_DQES.index)



plt.figure(figsize=(10, 6))

plt.plot(portfolio_value_DQVaR, label="DQ_VaR")
plt.plot(portfolio_value_DQES, label="DQ_ES")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.xlabel("Date")
plt.ylabel("Portfolio Value")

plt.legend()

plt.savefig("./output/DQ.png")


