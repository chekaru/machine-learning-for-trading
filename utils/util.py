"""Some utility code used in most files."""

import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import tee, izip

"""Return CSV file path given a stock ticker symbol."""
def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


"""Reads adjusted close stock data for given symbols from CSV files."""
def get_data(symbols, dates, addSPY=True):
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


"""Plot stock prices with a custom title and axis labels."""
def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

"""helper function for comparing stock data from two subsequent days iteratively"""
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
