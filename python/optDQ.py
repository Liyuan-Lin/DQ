import numpy as np
import cvxpy as cp

def opt_DQ_VaR(alpha, loss_ratio, tie_breaker=False, w_0=None):
    
    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[0]        # number of data = number of columns

    # calculate the VaR of each stock
    Y = np.zeros_like(loss_ratio)

    for i in range(n_stock):

        VaR = np.quantile(loss_ratio[:, i], 1 - alpha)

        Y[:, i] = loss_ratio[:, i] - VaR

    M = 50

    z = cp.Variable(n_data, integer=True)
    w = cp.Variable(n_stock)

    X = cp.sum(z)
    objective = cp.Minimize(X)
    # z_i is 0 or 1
    constraints = [z >= 0, z <= 1, w >= 0, cp.sum(w) == 1, Y @ w - M * z <= 0]

    prob = cp.Problem(objective, constraints)
    prob.solve()

    # output the optimal X
    opt_X = X.value

    if tie_breaker:

        w_plus = cp.Variable(n_stock)
        w_minus = cp.Variable(n_stock)

        z = cp.Variable(n_data, integer=True)

        X_norm = cp.sum(w_plus) + cp.sum(w_minus) 
        objective = cp.Minimize(X_norm)
        
        constraints = [z >= 0, z <= 1, cp.sum(z) <= opt_X,
                       w_plus >= 0, w_plus <= 1, w_minus >= 0, w_minus <= 1,
                       cp.sum(w_plus) - cp.sum(w_minus) == 0, 
                       w_0 + w_plus - w_minus >= 0,
                       (Y @ (w_0 + w_plus - w_minus)) - (M * z) <= 0]

        prob = cp.Problem(objective, constraints)
        prob.solve()
        
        opt_w = w_0 + w_plus.value - w_minus.value

    else:
            
        opt_w = w.value

    # calculate the optimal DQ_VaR
    opt_DQ_VaR = opt_X / n_data / alpha

    return opt_w, opt_DQ_VaR


def opt_DQ_ES(alpha, loss_ratio, tie_breaker=False, w_0=None):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio

    n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  
    n_data = loss_ratio.shape[0]        # number of data = number of columns

    # calculate the VaR of each stock
    Y = np.zeros_like(loss_ratio)

    for i in range(n_stock):

        VaR = np.quantile(loss_ratio[:, i], 1 - alpha)

        ES = np.mean(loss_ratio[ loss_ratio[:, i] > VaR,i])

        Y[:, i] = loss_ratio[:, i] - ES

    v = cp.Variable(n_stock)
    X = cp.sum(cp.maximum(Y @ v + np.ones(n_data), 0))
    objective = cp.Minimize(X)
    constraints = [v >= 0]
    prob = cp.Problem(objective, constraints)
    prob.solve()

    opt_X= X.value

    if tie_breaker:

        w= cp.Variable(n_stock)
        r = cp.Variable(1)
        X=cp.sum(cp.abs(w-w_0))
        objective = cp.Minimize(X)
        constraints = [r >= 0, w >= 0, w <= 1, cp.sum(w) == 1, cp.sum(cp.maximum(Y @ w + r, 0)) <= r*opt_X]
        prob = cp.Problem(objective, constraints)
        prob.solve()

        opt_w = w.value

    else:
       
        opt_w= v.value
        

    DQ_ES = opt_X / n_data / alpha

    return opt_w, DQ_ES
