import pandas as pd
import yfinance as yf


def dataLoader(tickers=None, start_date="2012-01-01", end_date=None):
    """
    Download stock data directly from Yahoo Finance
    
    Parameters:
        tickers: List of stock symbols, e.g., ['AAPL', 'MSFT', 'GOOGL']
                If None, uses the default stock list
        start_date: Start date in format "YYYY-MM-DD"
        end_date: End date in format "YYYY-MM-DD", if None then up to today
    
    Returns:
        DataFrame: DataFrame containing daily loss ratios
    """
    
    # If no tickers provided, use default list (based on stocks in data folder)
    if tickers is None:
        tickers = ['AAPL', 'AMZN', 'BRK-B', 'CVX', 'D', 'FCX', 'GE', 
                   'JNJ', 'MCD', 'MSFT', 'NEM', 'PFE', 'PG', 'SO', 
                   'T', 'UPS', 'VZ', 'WFC', 'WMT', 'XOM']
    
    print(f"Downloading data for {len(tickers)} stocks from Yahoo Finance...")
    
    # Download data (auto_adjust=False to get 'Adj Close' column)
    df_all = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=False)
    
    # Check if download was successful
    if df_all.empty:
        raise ValueError("No data downloaded. Please check your tickers and date range.")
    
    # Extract adjusted close prices
    if len(tickers) == 1:
        # For single stock, data structure is different
        if 'Adj Close' in df_all.columns:
            df_all = df_all[['Adj Close']].copy()
            df_all.columns = tickers
        else:
            raise ValueError("'Adj Close' column not found in downloaded data")
    else:
        # For multiple stocks, check if columns are MultiIndex
        if isinstance(df_all.columns, pd.MultiIndex):
            # yfinance returns MultiIndex columns for multiple tickers
            # Extract 'Adj Close' level
            if 'Adj Close' in df_all.columns.get_level_values(0):
                df_all = df_all['Adj Close'].copy()
            else:
                raise ValueError("'Adj Close' not found in MultiIndex columns")
        else:
            # Fallback for different structure
            if 'Adj Close' in df_all.columns:
                df_all = df_all[['Adj Close']].copy()
                df_all.columns = tickers
            else:
                raise ValueError("'Adj Close' column not found in downloaded data")
    
    # Drop missing values
    df_all = df_all.dropna()
    
    # Calculate daily loss ratio (negative of returns)
    df_all = - df_all.pct_change()
    
    # Only select data after the specified date
    df_all = df_all.loc[start_date:]
    
    # Drop missing values
    df_all = df_all.dropna()
    
    print(f"Download complete! Date range: {df_all.index[0]} to {df_all.index[-1]}")
    print(f"Number of stocks: {df_all.shape[1]}, Number of data points: {df_all.shape[0]}")
    
    return df_all