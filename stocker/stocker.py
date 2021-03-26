from abc import ABC
from datetime import datetime, timedelta
from typing import List

from pandas import DataFrame
from yfinance import Ticker
from yfinance import download


class Stock(ABC):
    """
    This is a class for capturing data from a single stock.

    Attributes:
        symbol (str): A stock ticker symbol.
        start (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
        end (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
    """
    # Initialization requires a ticker symbol
    def __init__(self, symbol: str, start: str=str((datetime.now()-timedelta(days=365))), end: str=str(datetime.now())):
        """
        The constructor for the Stock class.

        Parameters:
            symbol (str): A stock ticker symbol.
            start (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
            end (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
        """
        # Enforce capitalization
        self._ticker = symbol.upper().split(" ")[0]

        # Retrieval the financial data
        self._history = None
        self.start_date = start.split(" ")[0]
        self.end_date = end.split(" ")[0]
        self.stock_data = Ticker(self.ticker)
        self.calculate_stats()

    def __str__(self) -> str:
        return self._ticker

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.ticker!r}, start={self.start_date!r}, end={self.end_date!r} )"

        # Set various attributes
    def calculate_stats(self):
        """
        The method for calculating various metrics based on the stock's historic data.
        """
        self.beta = self.stock_data.info['beta']  # <--- Needs to be calculated, not pulled from website
        c = self.history.tail(1)['Close'].item()
        o = self.history.head(1)['Open'].item()
        self.return_pct = ((c - o)/o)
        self.average = {'open':self.history['Open'].mean(),
                         'close':self.history['Close'].mean(),
                         'high':self.history['High'].mean(),
                         'low':self.history['Low'].mean(),
                         'close-open':self.history['Close-Open'].mean(),
                         'high-low':self.history['High-Low'].mean()
                        }
        self.variance = {'open':self.history['Open'].var(),
                         'close':self.history['Close'].var(),
                         'high':self.history['High'].var(),
                         'low':self.history['Low'].var(),
                         'close-open':self.history['Close-Open'].var(),
                         'high-low':self.history['High-Low'].var()
                        }
        self.std_dev = {'open':self.history['Open'].std(),
                         'close':self.history['Close'].std(),
                         'high':self.history['High'].std(),
                         'low':self.history['Low'].std(),
                         'close-open':self.history['Close-Open'].std(),
                         'high-low':self.history['High-Low'].std()
                        }
        self.max = {'open':self.history['Open'].max(),
                    'close':self.history['Close'].max(),
                    'high':self.history['High'].max(),
                    'low':self.history['Low'].max(),
                    'close-open':self.history['Close-Open'].max(),
                    'high-low':self.history['High-Low'].max()
                    }
        self.min = {'open':self.history['Open'].min(),
                    'close':self.history['Close'].min(),
                    'high':self.history['High'].min(),
                    'low':self.history['Low'].min(),
                    'close-open':self.history['Close-Open'].min(),
                    'high-low':self.history['High-Low'].min()
                    }

    @property
    def stock_data(self) -> dict:
        return self._stock_data

    @stock_data.setter
    def stock_data(self, data):
        self._stock_data = data
        self._history = download(tickers=self.ticker, start=self.start_date, end=self.end_date)

    @property
    def history(self) -> DataFrame:
        self._history['Close-Open'] = self._history['Close'] - self._history['Open']
        self._history['High-Low'] = self._history['High'] - self._history['Low']
        return self._history

    @history.setter
    def history(self, history):
        self._history = history

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, symbol):
        self._ticker = symbol.upper()
        self.stock_data = Ticker(symbol)
        self.calculate_stats()

    def requery_data(self, start: str, end: str) -> DataFrame:
        return download(tickers=self.ticker, start=start.split(" ")[0], end=end.split(" ")[0])


class Market(ABC):
    """
    This is a class for putting together a basket of Stocks to represent a market.

    Attributes:
        symbol (str): A stock ticker symbol.
        rf (str): A stock ticker whose performance is used as the "risk-free rate" for determining market performance.
        start (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
        end (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
    """
    def __init__(self, symbols: List, rf: str='SPTI', start: str=str((datetime.now()-timedelta(days=365))), end: str=str(datetime.now())):
        # Enforce capitalization
        self.tickers = [x.upper() for x in symbols]
        self.stocks = []
        for t in self.tickers:
            self.stocks.append(Stock(t, start=start, end=end))

        self.risk_free = Stock(rf, start=start, end=end)

        # Retrieval the financial data
        self.start_date = start.split(" ")[0]
        self.end_date = end.split(" ")[0]
        self.calculate_stats()

    def __str__(self):
        return "Market consisting of " + str(self.tickers) + " with a risk-free alternative based on '" + self.risk_free.ticker + "'"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tickers!r}, rf={self.risk_free.ticker}, start={self.start_date!r}, end={self.end_date!r} )"

    def calculate_stats(self):
        open_stats = self.mkt_stats(self.stocks, 'open')
        close_stats = self.mkt_stats(self.stocks, 'close')
        high_stats = self.mkt_stats(self.stocks, 'high')
        low_stats = self.mkt_stats(self.stocks, 'low')
        self.average = {'open':open_stats[0], 'close':close_stats[0], 'high':high_stats[0], 'low':low_stats[0]}
        self.variance = {'open':open_stats[1], 'close':close_stats[1], 'high':high_stats[1], 'low':low_stats[1]}
        self.std_dev = {'open':open_stats[2], 'close':close_stats[2], 'high':high_stats[2], 'low':low_stats[2]}
        self.raw_return_pct = open_stats[3]  # calculated 3 times more than necessary, but saves iterating through again



    def mkt_stats(self, stocks: List, col: str) -> List:
        """
        Calculates a market-wide statistic.

        Parameters:
            stocks (List): a list containing multiple Stocks.
            col (str): The name of a column from the original dataframe which we are going to calculate.

        Returns:
            something -- still a work in progress.
        """
        c = 0
        avg = 0
        vari = 0
        stdv = 0
        ret = 0
        for stock in stocks:
            c += 1
            avg += stock.average[col]
            vari += stock.variance[col]
            stdv += stock.std_dev[col]
            ret += stock.return_pct
        return [avg/c, vari/c, stdv/c, ret/c]


class Pony(ABC):
    """
    A class to look at the performance of a stock in a given market.

    Attributes:
        symbol (str): A stock ticker symbol.
        market (List): A list of the symbols that make up the market.
        rf (str): A stock ticker whose performance is used as the "risk-free rate" for determining market performance.
        start (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
        end (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
    """
    def __init__(self, ticker: str, market: List, rf: str='SPTI', start: str=str((datetime.now()-timedelta(days=365))), end: str=str(datetime.now())):
        self.risk_free = rf
        self.start_date = start.split(" ")[0]
        self.end_date = end.split(" ")[0]
        self.market = Market(market, rf, start, end)
        self.stock = Stock(ticker, start, end)


    def __str__(self):
        return "Stock '" + self.stock.ticker + "' performing in a " + str(self.market)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.stock.ticker!r}, rf={self.risk_free}, start={self.start_date!r}, end={self.end_date!r} )"
