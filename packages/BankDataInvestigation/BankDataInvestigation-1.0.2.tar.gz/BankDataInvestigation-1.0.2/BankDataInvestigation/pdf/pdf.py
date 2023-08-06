import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def PDF_amount_transaction(trans_data : pd.DataFrame,
                    title : str = 'Probability distribution of the transaction amount',
                    clip_min : float = None,
                    clip_max : float = None,
                    bins : int = None,
                    client_id : int = None,
                    year : int = None,
                    log : bool = True,
                    client_col: str =None,
                    time_col: str = None, 
                    amount_col: str = None,
                    config: dict = None,
                    show_bins : bool = True
                   ):
    """A function that plots the probability distribution function of the transaction amount with respect to two optional parameters (client_ID, year). The x-axis gives the amount of transaction, and the y-axis the number of a client with x amount. It takes as arguments a dataframe, the names of three columns  "client_col", "amount_col", and the "time_col", or the name of the configuration class in the case of our data. Also, we can specify the range of the amount, the year we want to consider, the bins, and the logarithmic scale that is set as "True" by default."""

    
    if config is not None:
        client_col = config.customer_id
        amount_col = config.trans_amount
        time_col = config.trans_date
        
    trans_data[time_col] = trans_data[time_col].astype("datetime64")
    trans_data['year_trans'] = trans_data[time_col].dt.year
    trans_data['month_trans'] = trans_data[time_col].dt.month
    
    if ((client_id == None) & (year == None)):
        _plot(trans_data[amount_col], clip_min=clip_min, clip_max=clip_max, bins=bins, title=title, 
            xlabel='Transaction amount', ylabel='Number of Transactions', show_bins = show_bins)

    elif (client_id == None):
        _plot(trans_data[trans_data['year_trans'] == year][amount_col],
             clip_min=clip_min, clip_max=clip_max, bins=bins, title=title, 
            xlabel='Transaction amount', ylabel='Number of Transactions')

    elif (year == None):
        _plot(trans_data[trans_data[client_col] == client_id][amount_col],
                 clip_min=clip_min, clip_max=clip_max, bins=bins, title=title, 
            xlabel='Transaction amount', ylabel='Number of Transactions')
    else :
        _plot(trans_data[(trans_data[client_col] == client_id)
                            & (trans_data['year_trans'] == year)][amount_col],
             clip_min=clip_min, clip_max=clip_max, bins=bins, title=title, 
            xlabel='Transaction amount', ylabel='Number of Transactions')
    return



def PDF_transactions_client_month(trans_data : pd.DataFrame,
                                            client_col: str = None,
                                            config: dict = None,
                                           # bins : int = None,
                                            show_bins : bool = True
                                           ):

    """A function that plots the probability distribution function of transactions per "client-month" pair. The x-axis gives the number of transactions, and the y-axis the number of client-month pairs with x transactions for that client in that month. The function is named "PDF_transactions_client_month", and takes as arguments the dataframe, the column name, or the name of the configuration class in the case of our data."""
        
    if config is not None:
        client_col = config.customer_id
        amount_col = config.trans_amount
        time_col = config.trans_date
        
    trans_data[time_col] = trans_data[time_col].astype("datetime64")
    trans_data['year_trans'] = trans_data[time_col].dt.year
    trans_data['month_trans'] = trans_data[time_col].dt.month
    
    trans_month_ = trans_data.groupby([client_col, 'year_trans'])['month_trans']\
                    .value_counts().reset_index(name='nb_trans_month_account')
    fig, ax = plt.subplots(figsize = (20, 10))
    counts, bins, patches = ax.hist(trans_month_['nb_trans_month_account'],
                                    facecolor='g',
                                    edgecolor='gray',
                                    bins=None,
                                    log=True
                                  )
    xlabel ='Number of Transactions'
    ylabel ='Number of (client, month) with x transactions'
    title = 'The probability distribution function of transactions per "client-month" pair',


    if (show_bins == True):  
        ax.set_xticks(bins)
    plt.xticks( fontsize = 16, rotation = 60)
    plt.yticks(fontsize = 16, rotation = 0)
    
    ax.set_xlabel('%s' %xlabel, fontsize=20)
    ax.set_ylabel('%s' %ylabel, fontsize=20)

    ax.set_title('%s' %title, fontsize=25, color='darkolivegreen')

    ax.grid(alpha=0.75)
    return 





def _plot(col : pd.Series, 
        title : str,
        xlabel: str,
        ylabel: str,
        clip_min : float = None,
        clip_max : float = None,
        bins : int = None,
        show_bins : bool = True
        ):

    """it takes as argument a panda series (a column), bins and ranges and plot a histogram."""

    if   (clip_max == None):
        clip_max = col.max()
    if   (clip_min == None):
        clip_min = 0
    if   (bins == None):
        bins = 25

    fig, ax = plt.subplots(figsize = (20, 10))
    counts, bins, patches = ax.hist(col.clip(clip_min, clip_max),
                                    facecolor='g',
                                    edgecolor='gray',
                                    bins=bins,
                                    log=True
                                  )

    if (show_bins == True):  
        ax.set_xticks(bins)
    plt.xticks( fontsize = 16, rotation = 60)
    plt.yticks(fontsize = 16, rotation = 0)
    plt.xlim((clip_min, clip_max))
    ax.set_xlabel('%s' %xlabel, fontsize=25)
    ax.set_ylabel('%s' %ylabel, fontsize=25)

    ax.set_title('%s' %title, fontsize=30, color='darkolivegreen')

    ax.grid(alpha=0.75)
    return

