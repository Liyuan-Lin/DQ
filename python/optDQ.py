import numpy as np
import cvxpy as cp
import pandas as pd
import datetime

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


def opt_DQ_portfolio(alpha, loss_ratio, window_size=500):

    # alpha: confidence level
    # loss_ratio: 2-dimension loss ratio of the portfolio
    # window_size: training window size

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Convert index to datetime
    loss_ratio.index = pd.to_datetime(loss_ratio.index)

    n_stock = loss_ratio.shape[1]       # number of stocks = number of rows  

    start_year, start_month = 2014, 1
    end_year, end_month = int(today.split("-")[0]), int(today.split("-")[1])

    initial_value = 1000
    opt_w_DQVaR= {}
    opt_w_DQES= {}
    w = np.ones(n_stock) / n_stock

    for year in range(start_year, end_year + 1):

        for month in range(1, 13):

            # Use the first day of the month as reference
            current_date = pd.Timestamp(year=year, month=month, day=1)

            # Get training data up to the current date
            training_data = loss_ratio.loc[:current_date][-window_size:]

            # calculate the optimal investment weight that minimizes the DQ_VaR
            w, _ = opt_DQ_VaR(alpha, training_data.values, tie_breaker=True, w_0=w)
        
            # Get the first available date at or after current_date
            future_dates = loss_ratio.loc[current_date:].index
            if len(future_dates) > 0:
                opt_w_DQVaR[future_dates[0]] = w
                v, _ = opt_DQ_ES(alpha, training_data.values, tie_breaker=True, w_0=w)
                opt_w_DQES[future_dates[0]] = v


    # put optimal weight into a dataframe
    opt_w_DQVaR = pd.DataFrame(opt_w_DQVaR, index=loss_ratio.columns).T

    opt_w_DQES = pd.DataFrame(opt_w_DQES, index=loss_ratio.columns).T

    # calculate the monthly return 
    return_M = (1-loss_ratio).resample("ME").prod().loc["2014-01-01":]

    return_M.index = opt_w_DQVaR.index

    portfolio_value_DQVaR = (return_M * opt_w_DQVaR).sum(axis=1).cumprod(axis=0) * initial_value

    portfolio_value_DQVaR.index = pd.to_datetime(portfolio_value_DQVaR.index)

    portfolio_value_DQES = (return_M * opt_w_DQES).sum(axis=1).cumprod(axis=0) * initial_value

    portfolio_value_DQES.index = pd.to_datetime(portfolio_value_DQES.index)

    return portfolio_value_DQVaR, portfolio_value_DQES