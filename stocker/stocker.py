# Quandl for financial analysis, pandas and numpy for data manipulation
# fbprophet for additive models, #pytrends for Google trend data
import yfinance as yf
import pandas as pd
#import fbprophet
#import pytrends
#from pytrends.request import TrendReq
# Class for analyzing and (attempting) to predict future prices
# Contains a number of visualizations and analysis methods
class Stock:

    # Initialization requires a ticker symbol
    def __init__(self, symbol, period='1y', interval='1d'):
        # Enforce capitalization
        self._ticker = symbol.upper().split(" ")[0]

        # Retrieval the financial data
        self._period = period
        self._interval = interval
        self._history = None
        self.stock_data = yf.Ticker(self.ticker)
        self.calculate_stats()

        # Set various attributes
    def calculate_stats(self):
        self.beta = self.stock_data.info['beta']
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
    def stock_data(self):
        return self._stock_data

    @stock_data.setter
    def stock_data(self, data):
        self._stock_data = data
        self._history = yf.download(tickers=self.ticker, period=self.period, interval=self.interval)

    @property
    def history(self):
        self._history['Close-Open'] = self._history['Close'] - self._history['Open']
        self._history['High-Low'] = self._history['High'] - self._history['Low']
        return self._history

    @history.setter
    def history(self, history):
        self._history = history


    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        self._period = period
        self.history = yf.download(tickers=self.ticker, period=self.period, interval=self.interval)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        self._interval = interval
        self.history = yf.download(tickers=self.ticker, period=self.period, interval=self.interval)

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, symbol):
        self._ticker = symbol.upper()
        self.stock_data = yf.Ticker(symbol)
        self.calculate_stats()
