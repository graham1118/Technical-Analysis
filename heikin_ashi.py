import pandas as pd
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

name = input('Please enter a ticker: ')
ticker = yfinance.Ticker(name)
df_1 = ticker.history(interval="1d",period='190d')
print(df_1)
vol = df_1['Volume']
df_1['Date'] = range(df_1.shape[0])
df_1 = df_1.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

def plot_chart(df, volume):
	fig, ax = plt.subplots()
	ax.plot(volume , 'ko')

	ax1 = ax.twinx()
	candlestick_ohlc(ax1,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)
	
	
	
	fig.tight_layout()
	fig.show()

def convert_ha(df_org, complx = False, recursions=1):
	if complx:
		for i in range(recursions):
			for i in range(df_org.shape[0]):
				dt = df_org.copy()
				if i > 0:
					df_org.loc[df_org.index[i],'Open'] = (df_org['Open'][i-1] + df_org['Close'][i-1])/2
				df_org.loc[df_org.index[i],'Close'] = (df_org['Open'][i] + df_org['Close'][i] + df_org['Low'][i] +  df_org['High'][i])/4
				df_org.loc[df_org.index[i],'High'] = max([df_org['Open'][i],df_org['Close'][i],df_org['High'][i]])
				df_org.loc[df_org.index[i],'Low'] = min([dt['Open'][i],dt['Close'][i],dt['High'][i]])
			df_org = df_org.iloc[1:,:]
		return df_org
	else:
		new_df = df_org.copy()
		for i in range(df_org.shape[0]):
			if i > 0:
				new_df.loc[new_df.index[i],'Open'] = (df_org['Open'][i-1] + df_org['Close'][i-1])/2
			new_df.loc[new_df.index[i],'Close'] = (df_org['Open'][i] + df_org['Close'][i] + df_org['Low'][i] +  df_org['High'][i])/4
			new_df.loc[new_df.index[i],'High'] = max([df_org['Open'][i],df_org['Close'][i],df_org['High'][i]])
			new_df.loc[new_df.index[i],'Low'] = min([df_org['Open'][i],df_org['Close'][i],df_org['High'][i]])
		new_df = new_df.iloc[1:,:]
		return new_df

	
	
plot_chart(df_1, vol)
df_4 = convert_ha(df_1, complx=True, recursions=1)

plot_chart(df_4, vol)

plt.show()