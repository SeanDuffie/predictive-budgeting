""" stock.py

References:
- List of Stocks: https://www.nasdaq.com/market-activity/stocks/screener
- Classification: https://groww.in/blog/how-are-different-stocks-categorized+
    - https://www.synovus.com/personal/resource-center/financial-newsletters/2020/september/s-p-500-sectors
"""
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import yahoofinancials
import yfinance as yf


class Stock:
    """_summary_
    """
    def __init__(self, title) -> None:
        self.title = title
        self.refresh()

    def refresh(self) -> None:
        """ Updates the current stock data from YFinance """
        print("Get Ticker")
        self.stock = yf.Ticker(self.title)
        print("Get History")
        self.df = self.stock.history()

        # print("Yahoo Financials")
        # data = yahoofinancials.YahooFinancials(self.title)
        # print("Financial Statements")
        # self.financials = data.get_financial_stmts(frequency='quarterly', statement_type='income')

        # self.SMA("Close", 100)
    def get_updown(self):
        updown = self.stock.get_upgrades_downgrades()

        print(f"{self.title} | UP/DOWN")
        print(updown)
        print("\n")
        return updown

    def get_target(self):
        target = self.stock.get_analyst_price_target()

        print(f"{self.title} | TARGET")
        print(target)
        print("\n")
        return target

    def get_bal_sheet(self):
        balsheet = self.stock.get_balance_sheet()

        print(f"{self.title} | BALANCE SHEET")
        print(balsheet)
        print("\n")
        return balsheet

    def get_calendar(self):
        calendar = self.stock.get_calendar()

        print(f"{self.title} | CALENDAR")
        print(calendar)
        print("\n")
        return calendar

    # def get_financials(self):
    #     financials = self.financials

    #     print(f"{self.title} | FINANCIALS")
    #     print(financials)
    #     print("\n")
    #     return financials

    def get_all(self):
        # self.get_updown()
        # self.get_target()
        # self.get_bal_sheet()
        # self.get_calendar()
        # self.get_financials()
        pass

    def SMA(self, feature: str, window_size: int) -> pd.DataFrame:
        """ Simple Moving Average
            Calculates the average of a certain feature over a given window of time

            Parameters:
            - feature (str) - what column to measure
            - window_size (int) - what time period to measure

            Returns:
            - df - pandas DataFrame with new feature column appended
        """
        new_col = f"MA_{feature}_{window_size}"
        self.df[new_col] = self.df[feature].rolling(window=window_size).mean()
        return self.df

    def Volatility(self, feature: str, window_size: int) -> pd.DataFrame:
        """ Volatility
            Calculates the Volatility of a certain feature over a given window of time

            Parameters:
            - feature (str) - what column to measure
            - window_size (int) - what time period to measure

            Returns:
            - df - pandas DataFrame with new feature column appended
        """
        new_col = f"VOL_{feature}_{window_size}"
        returns = np.log(self.df[feature]/self.df[feature].shift())
        returns.fillna(0, inplace=True)
        self.df[new_col] = returns.rolling(window=window_size).std()*np.sqrt(window_size)
        return self.df

    def RSI(self, feature: str, window_size: int) -> pd.DataFrame:
        """ Relative Strength Index
            Calculates the Momentum of the stock based on previous data

            Parameters:
            - feature (str) - what column to measure
            - window_size (int) - what time period to measure

            Returns:
            - df - pandas DataFrame with new feature column appended
        """
        new_col = f"RSI_{feature}_{window_size}"
        delta = self.df[feature].diff()
        delta = delta [1:]
        up, down = delta.clip(lower=0), delta.clip(upper=0)
        roll_up = up.rolling(window_size).mean()
        roll_down = down.abs().rolling(window_size).mean()
        rs = roll_up / roll_down
        rsi = 100 - (100 / (1 + rs))
        self.df[new_col] = rsi
        return self.df

    def print_info(self):
        """
        returns:
        {
        'quoteType': 'EQUITY',
        'quoteSourceName': 'Nasdaq Real Time Price',
        'currency': 'USD',
        'shortName': 'Microsoft Corporation',
        'exchangeTimezoneName': 'America/New_York',
        ...
        'symbol': 'MSFT'
        }
        """

        # get stock info
        print(self.stock.info)

    def print_history(self):
        """
        returns:
                    Open    High    Low    Close      Volume  Dividends  Splits
        Date
        1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
        1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
        ...
        2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
        2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
        """
        # get historical market data, here max is 5 years.
        print(self.stock.history(period="max"))

    def plot(self, start: datetime.datetime = None, stop: datetime.datetime = None):
        if start is None:
            start = self.df.index[0]
        if stop is None:
            stop = self.df.index[len(self.df.index)-1]
        # df = self.df.index.to_frame().reset_index(drop=True)

        # TODO: Replace this with useful data
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex = True)
        fig.suptitle(f"{self.title} over time")
        ax1.plot(self.df.index, self.df["Open"])
        ax2.plot(self.df.index, self.df["Close"], 'tab:orange')
        ax3.plot(self.df.index, self.df["High"], 'tab:green')
        ax4.plot(self.df.index, self.df["Low"], 'tab:red')

        for ax in fig.get_axes():
            ax.label_outer()
        fig.autofmt_xdate()
        fig.show()
        a = input("Hit enter to quit...")

if __name__ == "__main__":
    # s1 = Stock("T")
    # s1.print_history()

    print("Started")
    s2 = Stock("MSFT")
    print("History")
    s2.print_history()
    s2.plot()
    # print("All")
    # s2.get_all()

    # s3 = Stock("VFIAX")
    # s3.print_history()
