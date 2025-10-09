# Diversification Quotient Implementation in Python (Weekly Updated)

This is the implementation of the Diversification Quotient (DQ) in Python that generates weekly updates of the DQ value.

![DQ_VaR and DQ_ES](output/DQs.png)
![Portfolio](output/DQ_portfolio.png)

## Usage

To run the code, you need to have Python installed. You can then run the following command:
```bash
python example.py
```

## example.py


In example.py, we calculate the DQ VaR and DQ ES values for the equal-weighted portfolio of 20 stocks (AAPL, AMZN, BRK-B, CVX, D, FCX, GE, JNJ, MCD, MSFT, NEM, PFE, PG, SO, T, UPS, VZ, WFC, WMT, XOM) with a rolling window of 500 days starting from 2014/1/2 and update the values every week.
In addition, we optimize the portfolio weights in each month with a rolling window of 500 days.  That is, at the beginning of each month starting from 2014/1/2, we use the preceding 500 trading days to compute the optimal portfolio weights by minimizes DQ based on VaR and ES. The portfolio is rebalanced every month. 


## calDQ.py

### DQ_VaR

- The `DQ_VaR` function calculates the value of $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$.
- **Input:**
  - `loss_ratio`: A matrix of loss ratios of n stocks, with each row representing a data record.
  - `alpha`: The significance level for $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.
  - `window_size`: The size of the rolling window.
- **Output:**
  - A sequence of real numbers representing the value of $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$ calculated with a rolling window of 500 days.

### DQ_ES

- The `DQ_ES` function calculates the value of $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.
- **Input:**
  - `loss_ratio`: A matrix of loss ratios of n stocks, with each row representing a data record.
  - `alpha`: The significance level for $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.
  - `window_size`: The size of the rolling window.
- **Output:**
  - A sequence of real numbers representing the value of $\mathrm{DQ}^{\mathrm{ES}}_\alpha$ calculated with a rolling window of 500 days.

---




## optDQ.py

### opt_DQ_VaR

- The `opt_DQ_VaR` function is used to find the optimal portfolio weight that minimizes $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$.
- **Input:**
  - `alpha`: The significance level for $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$.
  - `loss_ratio`: A matrix of loss ratios of n stocks, with each row representing a data record.
  - `tie_breaker`: (Optional) Set to `True` if tie-breaking is needed.
  - `w_0`: (Optional) A vector representing the benchmark portfolio weights.
- **Output:**
  - A tuple `(opt_w, opt_DQ_VaR)` where:
    - `opt_w`: The optimal weight vector that minimizes $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$.
    - `opt_DQ_VaR`: The corresponding minimized value of $\mathrm{DQ}^{\mathrm{VaR}}_\alpha$.

### opt_DQ_ES

- The `opt_DQ_ES` function is used to find the optimal portfolio weight that minimizes $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.
- **Input:**
  - `alpha`: The significance level for DQ.
  - `loss_ratio`: A matrix of loss ratios of n stocks, with each row representing a data record.
  - `tie_breaker`: (Optional) Set to `True` if tie-breaking is needed.
  - `w_0`: (Optional) A vector representing the benchmark portfolio weights.
- **Output:**
  - A tuple `(opt_w, opt_DQ_ES)` where:
    - `opt_w`: The optimal weight vector that minimizes $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.
    - `opt_DQ_ES`: The corresponding minimized value of $\mathrm{DQ}^{\mathrm{ES}}_\alpha$.




If you have specific questions about using this code, implementing it, or interpreting its results, feel free to contact me at Liyuan.Lin@gmail.com!
