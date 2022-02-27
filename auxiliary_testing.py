import requests as r
import yahoo_fin.stock_info as yfn
import yfinance as yf
import pandas as pd
import all_tickers as at
from ta.momentum import RSIIndicator, ROCIndicator
from ta.volatility import BollingerBands
from matplotlib import pyplot as plt 
import math
import datetime
import all_tickers as at



import time 

print('hi', end='\r')
time.sleep(2)
print(' ',end='\r')
#print(end='\r')