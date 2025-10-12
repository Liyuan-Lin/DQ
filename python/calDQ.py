import numpy as np
import pandas as pd
import cvxpy as cp


def DQ_VaR(alpha, loss_ratio, window_size=500):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio
    # window_size: training window size

    n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[0]        # number of data = number of columns

    start_idx = window_size
    end_idx = n_data

    DQ_VaR = {}

    for i in range(start_idx, end_idx):

        VaR = np.zeros(n_stock)
        time = loss_ratio.index[i]

        values_allStocks = loss_ratio.iloc[i-window_size:i, :]

        for j in range(n_stock):
            
            values = values_allStocks.iloc[:, j]

            VaR[j] = np.quantile(values, 1 - alpha)
        
        DQ_VaR[time] = np.sum((np.sum(values_allStocks, axis=1) > np.sum(VaR))) / window_size / alpha

    df_DQ_VaR = pd.DataFrame.from_dict(DQ_VaR, orient='index')   

    return df_DQ_VaR



def DQ_ES(alpha, loss_ratio, window_size=500):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio
    # window_size: training window size

    n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[0]        # number of data = number of columns

    start_idx = window_size
    end_idx = n_data

    DQ_ES = {}

    for i in range(start_idx, end_idx):

        values_allStocks = loss_ratio.iloc[i-window_size:i, :]

        Y = np.zeros_like(values_allStocks)

        time = loss_ratio.index[i]

        for j in range(n_stock):
            
            values = values_allStocks.iloc[:, j]

            VaR = np.quantile(values, 1 - alpha)

            ES = np.mean(values[values > VaR])

            Y[:, j] = values - ES

        r = cp.Variable()
        X = cp.sum(cp.maximum(r * cp.sum(Y, axis=1) + np.ones(window_size), 0))
        objective = cp.Minimize(X)  
        constraints = [r >= 0]
        prob = cp.Problem(objective, constraints)
        prob.solve()

        DQ_ES[time] = X.value / window_size / alpha 


    df_DQ_ES = pd.DataFrame.from_dict(DQ_ES, orient='index')

    return df_DQ_ES


