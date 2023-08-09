import numpy as np
import cvxpy as cp

def opt_DQ_VaR(alpha, loss_ratio):
    
    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[0]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[1]        # number of data = number of columns

    # calculate the VaR of each stock
    Y = np.zeros_like(loss_ratio)

    for i in range(n_stock):

        VaR = np.quantile(loss_ratio[i, :], 1 - alpha)

        Y[i, :] = loss_ratio[i, :] - VaR

    M = 50

    z = cp.Variable(n_data, integer=True)
    w = cp.Variable(n_stock)

    X = cp.sum(z)
    objective = cp.Minimize(X)
    # z_i is 0 or 1
    constraints = [z >= 0, z <= 1, w >= 0, cp.sum(w) == 1, w @ Y - M * z <= 0]

    prob = cp.Problem(objective, constraints)
    prob.solve()

    # output the optimal portfolio
    opt_w = w.value

    # output the optimal X
    opt_X = X.value

    # calculate the optimal DQ_VaR
    opt_DQ_VaR = opt_X / n_data / alpha

    return opt_w, opt_DQ_VaR


def opt_DQ_ES(alpha, loss_ratio):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[0]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[1]        # number of data = number of columns

    # calculate the VaR of each stock
    Y = np.zeros_like(loss_ratio)

    for i in range(n_stock):

        VaR = np.quantile(loss_ratio[i, :], 1 - alpha)

        ES = np.mean(loss_ratio[i, loss_ratio[i, :] > VaR])

        Y[i, :] = loss_ratio[i, :] - ES

    v = cp.Variable(n_stock)
    X = cp.sum(cp.maximum(v @ Y + np.ones(n_data), 0))
    objective = cp.Minimize(X)
    constraints = [v >= 0]
    prob = cp.Problem(objective, constraints)
    prob.solve()

    v = v.value

    w = v / np.sum(v)

    DQ_ES = X.value / n_data / alpha

    return w, DQ_ES