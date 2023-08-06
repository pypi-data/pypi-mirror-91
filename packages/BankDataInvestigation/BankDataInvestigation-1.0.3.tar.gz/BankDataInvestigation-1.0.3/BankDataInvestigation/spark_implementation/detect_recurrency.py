import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthEnd

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import pandas_udf, PandasUDFType, col, to_timestamp


        
   

def DetectRecurrency(
                      amount_tolerance : float=0.01, 
                      period_tolerance : int=6,
                      n_days : int=3,
                      client_col: str =None,
                      time_col: str = None, 
                      amount_col: str = None,
                      config: dict = None
                      ):
    
    """ It is Pandas function that will be called using "pandas function APIs". It takes as arguments an integer "period_tolerance" that is the minimum number of occuracy of an amount that it be selected, a float number "amount_tolerance" that is the accepted range for the amount, an integer "n_days" that is the accepted variance in the payement day. It returns a dataframe of all the recurring amount. 
    To  call it on pyspark dataframe, we specify the parameters and save in a variable x = DetectRecurrency(...), nd we call it s follow 
          account_table = account_table.groupby('account_id').applyInPandas(sdr.PysparkDetectRecurrecy, schema=
     "account_id long, trans_amount double, trans_date timestamp, freq double, rec boolean")."""
    
    if config is not None:
        client_col = config.customer_id
        amount_col = config.trans_amount
        time_col = config.trans_date

    #Creation of the new columns
    def rb(trans_data : pd.DataFrame):
        number_occuracy_big, account_table = _complete_table(trans_data, 
                                    period_tolerance=period_tolerance,
                                    client_col=client_col, 
                                    time_col=time_col, 
                                    amount_col=amount_col,
                                    config=config)

        # Check the time rules for recurrency
        number_occuracy_big['day_of_month_cond'] = number_occuracy_big[amount_col].map(lambda x: 
                            (number_occuracy_big[(number_occuracy_big[amount_col] > x - x * amount_tolerance)
                                        & 
                        (number_occuracy_big[amount_col] <= x + x * amount_tolerance)]
                         .day_of_month.value_counts().count() < n_days))

        number_occuracy_big['number_day_end_month_cond'] = number_occuracy_big[amount_col].map(lambda x:
               (number_occuracy_big[(number_occuracy_big[amount_col] > x - x * amount_tolerance)
                                        & 
                        (number_occuracy_big[amount_col] <= x + x * amount_tolerance)]
                         .number_day_end_month.value_counts().count() < n_days))

        number_occuracy_big['number_business_day_end_month_cond'] = number_occuracy_big[amount_col].map(lambda x:
                      (number_occuracy_big[(number_occuracy_big[amount_col] >= x - x * amount_tolerance)
                                        & 
                        (number_occuracy_big[amount_col] <= x + x * amount_tolerance)]
                         .number_business_day_end_month.value_counts().count() < n_days))

        number_occuracy_big['rec'] = ((number_occuracy_big['day_of_month_cond'] == True) |
                            (number_occuracy_big['number_day_end_month_cond'] == True) |
                            (number_occuracy_big['number_business_day_end_month_cond'] == True))

        number_occuracy_big = number_occuracy_big.drop([#'number_occuracy_big',
                                       'number_day_end_month_cond',
                                      'day_of_month_cond',
                                     'number_business_day_end_month_cond',
                                        "day_of_month",
                                        "end_of_month",
                                        'number_day_end_month',
                                        'number_business_day_end_month'
                                   ], axis=1)

        return number_occuracy_big[number_occuracy_big['rec'] == True]
    return rb




def _complete_table(
                    trans_data : pd.DataFrame,
                    amount_tolerance : float=0.01,
                    period_tolerance : int=5,
                    client_col: str =None,
                    time_col: str = None, 
                    amount_col: str = None,
                    config: dict = None
                   ):
    """It takes as arguments the dataframe of a choosen customer, an integer "period_tolerance" that is 
    the minimum number of occuracy of an amount that it be selected, a float number "amount_tolerance" that is the accepted range 
    for the amount, an integer "n_days" that is the accepted variance in the payement day. It returns the same table with additionnal 
    columns that are needed by the functions "DetectRecurrencyI" and "DetectRecurrencyII"."""    
    

    if config is not None:

        client_col = config.customer_id
        amount_col = config.trans_amount
        time_col = config.trans_date
        
    
    # Creation of the number of occuracy column
    trans_data['freq'] = trans_data[amount_col].map(lambda x: 
                                        np.sum((trans_data[amount_col] >= x - x * amount_tolerance)
                                                        & 
                                                (trans_data[amount_col] <= x + x * amount_tolerance)))

    
    # Creation of the time columns
    trans_data[time_col] = trans_data[time_col].astype('datetime64')

    
    trans_data['end_of_month'] = pd.to_datetime(
        trans_data[time_col], format="%Y%m") + MonthEnd(0)
    trans_data['day_of_month'] = trans_data[time_col].dt.day
    

    trans_data['number_day_end_month'] = trans_data.end_of_month.dt.day - \
        trans_data.day_of_month
    #
    A = [d.date() for d in trans_data[time_col]]
    B = [d.date() for d in trans_data['end_of_month']]
    trans_data['number_business_day_end_month'] = np.busday_count(A, B)
    
    # Selecting the condidate for Recurring values 
    number_occuracy_big = trans_data[trans_data['freq'] >= period_tolerance].copy()

    return number_occuracy_big, trans_data

