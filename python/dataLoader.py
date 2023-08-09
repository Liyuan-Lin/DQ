import pandas as pd

import os

path = "./data/"

def dataLoader(path):

    file_list = os.listdir(path)

    # Append all adjusted close prices into a dataframe
    for file in file_list:


        df = pd.read_csv(path + file)
        
        df = df[["Date", "Adj Close"]]

        df = df.rename(columns={"Adj Close": file[:-4]})

        if file == file_list[0]:
                
            df_all = df
            
        else:
                
            df_all = pd.merge(df_all, df, on="Date", how="outer")

    # Drop the rows with missing values
    df_all = df_all.dropna()

    # Calculate the daily loss ratio
    df_all = df_all.set_index("Date")

    df_all = - df_all.pct_change()

    df_all = df_all.dropna().T

    return df_all