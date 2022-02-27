def Shallow_Dip(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[min(RSI[-10:-1]), 30],
			[sum(bbw[-5:-1])/len(bbw[-5:-1]), 0.9*sum(bbw[-15:-10])/len(bbw[-15:-10])],
			[Close[-1], Open[-1]],
			[Open[-1], Low[-1]],
			[Open[-2], Close[-2]],
			[Close[-2], 1.05*Open[-2]]] #Very thin red HA candlesticks followed by upwards spike
def Strong_Dip(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[Close[Low.index(min(Low[-8:], default="EMPTY"))], Open[Low.index(min(Low[-8:], default="EMPTY"))]], #[High[Low.index(min(Low[-8:], default="EMPTY"))], Open[Low.index(min(Low[-8:], default="EMPTY"))]],
			[Open[Low.index(min(Low[-8:], default="EMPTY"))+1], Close[Low.index(min(Low[-8:], default="EMPTY"))+1]],
			[Open[Low.index(min(Low[-8:], default="EMPTY"))+1], Low[Low.index(min(Low[-8:], default="EMPTY"))+1]],
			[25, High.index(max(High))],
			[min(Low[:High.index(max(High))], default="EMPTY"), 0.7*max(High, default="EMPTY")],
			[min(ROC[High.index(max(High)):], default="EMPTY"), -18]]

			#Strong Dip, followed by strong HA candelsticks
			#Sell after the recover flattens out
def Extreme_Dip(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[Close[-2], Close[-1]],
			[Close[-2], 0.5 *max(High, default="EMPTY")],
			[Close[0], 0.5*max(High, default="EMPTY")]]#Extreme Dip
def Value(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[min(RSI[-10:-1], default="EMPTY"), 50],
			[24, min(RSI[-10:-1], default="EMPTY")],
			[Close[-10], Close[-1]]]
def Straddle(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[70, min(RSI[-10:-1], default="EMPTY")],
			[BBW[-1], 0.65*BBW[-5]]]
def Short(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[70, RSI[-5]],
			[70, RSI[-1]],
			[BBW[-1], 0.85*sum(BBW[-10:-5])/len(BBW[-10:-5])]]
def Divergence(RSI=None, ROC=None,BBW=None,High=None,Close=None,Low=None,Open=None):
	return [[RSI[-15], 0.9*RSI[-1]],
			[RSI[-1], 45],
			[BBW[-1], 0.85*BBW[-5]]]
def get_ndaq():
	import yfinance as yf
	import yahoo_fin.stock_info as yfn
	import pandas as pd
	hist = yf.Ticker('NDAQ').history(period="253d")
	nasdaq_now =hist["Close"][-1]
	nasdaq_year_ago = hist["Close"][0]
	nasdaq_change = 100*((nasdaq_now/nasdaq_year_ago) - 1)
	return nasdaq_change

### Screen on TradingView for EV/EDIBA
### First 30 RSI after a crazy peak and recovery downwards (titled, 'QS')

strategies = {'Shallow Dip': ['0.15 < month3ChangePercent(-1) 1',
			  			   '-0.10 < day5ChangePercent(-1) < 0 1',
						   'Losers',
						   'Active', 
						   Shallow_Dip],
			  'Strong Dip': [Strong_Dip,
			  				 '0 < peRatio(-1) 0'],
			  'Extreme Dip':[Extreme_Dip],
			  'Value':[Value],#'3 < latestPrice(-1) < 30 1',
						#'0 < month3ChangePercent(-1) < 0.3 1',
						#'0 < peRatio(-1) < 18 1',
						#'avg10Volume(-4) < 0.6*avg30Volume(-4) 1'],
			  'Short': ['18 < latestPrice(-1) < 80 1',
			  					 '0.15 < month1ChangePercent(-1) 1',
			  					 'avg10Volume(-4) < 0.8*avg30Volume(-4) 1',
			  					 Short],
			  'Divergence': ['0.2 < year1ChangePercent(-1) 1',
			  						   '-0.15 < month3ChangePercent(-1) < -0.05 1',
			  				  		   '-0.09 < month1ChangePercent(-1) < 0 1',
			  				  		   Divergence],
			  'Straddle':['avg10Volume(-2) < 0.8*avg30Volume(-2) 1',
			  			   '0.2 < month1ChangePercent(-1) 1',
			  			   'day5ChangePercent(-1) < 1 0',
			  			   Straddle],
			  'SPCE':['SPCE'],
			  'BRS':'',
			  'Previous Screens':''
			  }





