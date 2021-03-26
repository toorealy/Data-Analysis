import pytest

from stocker.stocker import *

test_stock = Stock("tsla")

def test_stock_ticker_uppercase():
    assert test_stock.ticker == "TSLA"

def test_stock_ticker_type():
    assert type(test_stock.ticker) == type("string")

test_market = Market(['msft', 'tsla', 'spy'])

def test_market_uppercase():
    assert test_market.stocks == ['MSFT', 'TSLA', 'SPY']

def test_market_types():
    assert type(test_market.stocks[0]) == type(test_stock)
