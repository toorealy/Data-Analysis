from abc import ABC
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import yfinance as yf


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
        self.stock_data = yf.Ticker(self.ticker)
        self.calculate_stats()

    def __str__(self) -> str:
        return self._ticker + " from " + str(self.start_date) + " to " + str(self.end_date)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.ticker!r}, start={self.start_date!r}, end={self.end_date!r} )"

        # Set various attributes
    def calculate_stats(self):
        """
        The method for calculating various metrics based on the stock's historic data.
        """
        self.beta = self.stock_data.info['beta']
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
    '''
    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start: str):
        try:
            parsed = start.split("-")
            y = parsed[0]
            m = parsed[1]
            d = parsed[2]
            self.history = self.requery_data(start, self.end_date)
        except IndexError:
            print("Your date is not in the yyyy-mm-dd format")
    '''

    @property
    def stock_data(self) -> dict:
        return self._stock_data

    @stock_data.setter
    def stock_data(self, data):
        self._stock_data = data
        self._history = yf.download(tickers=self.ticker, start=self.start_date, end=self.end_date)

    @property
    def history(self) -> pd.DataFrame:
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
        self.stock_data = yf.Ticker(symbol)
        self.calculate_stats()

    def requery_data(self, start: str, end: str) -> pd.DataFrame:
        return yf.download(tickers=self.ticker, start=start.split(" ")[0], end=end.split(" ")[0])

class Market(ABC):
    """
    This is a class for putting together a basket of Stocks to represent a market.

    Attributes:
        symbol (str): A stock ticker symbol.
        rf (str): A stock ticker whose performance is used as the "risk-free rate" for determining market performance.
        start (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
        end (str): A date in yyyy-mm-dd format. This data is the beginning of a period of time to query stock data.
    """
    def __init__(self, symbols: List, rf: str='SPTI', start: datetime=str(datetime.now()), end: datetime=str((datetime.now()-timedelta(days=365)))):
        # Enforce capitalization
        tickers = [x.upper() for x in symbols]
        self.stocks = []
        for t in tickers:
            self.stocks.append(Stock(t, period=period, interval=interval))

        self.risk_free = Stock(rf, period=period, interval=interval)

        # Retrieval the financial data
        self.start_date = start
        self.end_date = end
        self._history = None
        self.stock_data = None #yf.Ticker(self.ticker)
        self.calculate_stats()
    def calculate_stats(self):
        pass
