import numpy as np
import cvxpy as cp


def DQ_VaR(alpha, loss_ratio):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[0]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[1]        # number of data = number of columns

    # calculate the VaR of each stock
    VaR = np.zeros(n_stock)

    for i in range(n_stock):

        VaR[i] = np.quantile(loss_ratio[i, :], 1 - alpha)

    # calculate DQ_VaR
    DQ_VaR = np.sum((np.sum(loss_ratio, axis=0) > np.sum(VaR))) / n_data / alpha 

    return DQ_VaR


def DQ_ES(alpha, loss_ratio):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[0]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[1]        # number of data = number of columns

    Y = np.zeros_like(loss_ratio)

    for i in range(n_stock):
        
        VaR = np.quantile(loss_ratio[i, :], 1 - alpha)

        ES = np.mean(loss_ratio[i, loss_ratio[i, :] > VaR])

        Y[i, :] = loss_ratio[i, :] - ES

    r = cp.Variable()
    X = cp.sum(cp.maximum(r * cp.sum(Y, axis=0) + np.ones(n_data), 0))
    objective = cp.Minimize(X)
    constraints = [r >= 0]
    prob = cp.Problem(objective, constraints)
    prob.solve()

    DQ_ES = X.value / n_data / alpha 

    return DQ_ES


