from dataLoader import dataLoader
from optDQ import opt_DQ_portfolio
from calDQ import DQ_VaR, DQ_ES

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import cvxpy as cp


alpha = 0.05
window_size = 500
today = datetime.datetime.now().strftime("%Y-%m-%d")

loss_ratio = dataLoader(start_date="2012-01-01", end_date=today)

df_DQ_VaR = DQ_VaR(alpha, loss_ratio, window_size)
df_DQ_ES = DQ_ES(alpha, loss_ratio, window_size)

portfolio_value_DQVaR, portfolio_value_DQES = opt_DQ_portfolio(alpha, loss_ratio, window_size)

plt.figure(figsize=(10, 6))

plt.plot(df_DQ_VaR, label=f"DQ_VaR")
plt.plot(df_DQ_ES, label=f"DQ_ES")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.title("DQ Values (Updated Weekly)")

plt.legend()

plt.savefig("./output/DQs.png")


plt.figure(figsize=(10, 6))

plt.plot(portfolio_value_DQVaR, label=f"DQ_VaR: {terminal_wealth_DQVaR:,.2f}")
plt.plot(portfolio_value_DQES, label=f"DQ_ES: {terminal_wealth_DQES:,.2f}")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.title("Wealth Processes for Portfolio Optimized by DQ_VaR and DQ_ES (Updated Weekly)")
plt.legend()

plt.savefig("./output/DQ_portfolio.png")





