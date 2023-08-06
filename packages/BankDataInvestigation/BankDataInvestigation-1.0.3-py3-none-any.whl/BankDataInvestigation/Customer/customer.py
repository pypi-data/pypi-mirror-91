
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def number_of_customers(trans_data : pd.DataFrame, 
						client_col: str = None, 
						config: dict = None):

    '''Takes a dataframe, and the name of the column of the customer identity or the name of configuration class and returns the number of distinct element in that column.'''

    if config is not None:
        client_col = config.customer_id
    return trans_data[client_col].nunique()
    

def number_of_transactions(trans_data : pd.DataFrame, 
                           amount_col: str = None, 
                           config: dict = None,
                           per_year = False
                        ):
    '''Takes a dataframe, and the name of the column  of the transaction identity or the name of configuration class and returns the number of distinct element in that column. It also allows to have he number of distinct element in that column for each year if the argument "per_year" is set "True".'''

    if config is not None:
        time_col = config.trans_date
        amount_col = config.trans_amount
    if per_year == True : 
        
        trans_data[time_col] = trans_data[time_col].astype('datetime64')
        trans_data['year_trans'] = trans_data.trans_date.dt.year

        return trans_data.groupby('year_trans')[amount_col].nunique()

    return trans_data[amount_col].nunique()

def number_of_active_accounts(trans_data : pd.DataFrame, 
                              year: int = None,
                              month: int = None,
                              time_col: str = None, 
                              client_col: str =None,
                              config: dict = None
                             ):

    ''' Takes a dataframe, a month and/or a year and the name of the column or the name of the configuration class and returns the number of account that has at least one transaction in the given period'''

    if config is not None:
        time_col = config.trans_date
        client_col = config.customer_id
        amount_col = config.trans_amount

    trans_data =trans_data.dropna(subset=[amount_col]).copy()
    trans_data[time_col] = trans_data[time_col].astype("datetime64")
    trans_data['year_trans'] = trans_data[time_col].dt.year
    trans_data['month_trans'] = trans_data[time_col].dt.month

    if ((month == None) & (year == None)):
        return trans_data.groupby(client_col).count().shape[0]
    elif (month == None):
        return trans_data[(trans_data['year_trans'] == year )].groupby(client_col).count().shape[0]
    elif (year == None):
        return trans_data[(trans_data['month_trans'] == month )].groupby(client_col).count().shape[0]
    else :
        return trans_data[(trans_data['year_trans'] == year ) &
               (trans_data['month_trans'] == month ) ].groupby(client_col).count().shape[0]
    






    
