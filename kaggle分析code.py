#導入模組
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")
%matplotlib inline
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
# For reading stock data from yahoo
from pandas_datareader.data import DataReader

# For time stamps
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")
#導入btc data
dateparse = lambda dates: pd.datetime.strptime(dates, '%d-%m-%Y')
btc=pd.read_csv('../input/meme-cryptocurrency-historical-data/Bitcoin.csv',parse_dates=['Date'],index_col='Date', date_parser=dateparse)
btc = btc.iloc[::-1]
btc.tail(5)
#設定最大值
maxValue=btc[btc['Close']==max(btc.Close)]
print("Highiest value of bitcoin")
maxValue
#展示
btc.describe()
btc.info()
#導入dogecoin data
doge=pd.read_csv('../input/meme-cryptocurrency-historical-data/Meme Coin/Dogecoin.csv',parse_dates=['Date'],index_col='Date', date_parser=dateparse)
doge = doge.iloc[::-1]
doge.tail(5)
#設定數值
maxValue=doge[doge['Close']==max(doge.Close)]
print("Highiest value of Dogecoin")
maxValue
#導入bitconnect Data
bit=pd.read_csv('../input/meme-cryptocurrency-historical-data/Dead Coin/bitconnect.csv',parse_dates=['Date'],index_col='Date', date_parser=dateparse)
bit=bit.iloc[:,1:7]
bit = bit.iloc[::-1]
bit=bit.iloc[:1580]
bit18=bit[:609]
bit.tail(5)
#設定數值
maxValue=bit[bit['Close']==max(bit.Close)]
print("Highiest value of Bitconnect")
maxValue
#導入ETH DATA
eth=pd.read_csv('../input/meme-cryptocurrency-historical-data/Ethereum.csv',parse_dates=['Date'],index_col='Date', date_parser=dateparse)
eth = eth.iloc[::-1]
eth.tail(5)
#設定數值
maxValue=eth[eth['Close']==max(eth.Close)]
print("Highiest value of Ethereum")
maxValue

#線圖可視化
btc18=to2018(btc)
eth18=to2018(eth)
crypto=["Bitcoin 2018","Bitcoin","Ethereum 2018","Ethereum","Bitconnect 2018","Dogecoin"]
cryptoDf=[btc18,btc,eth18,eth,bit18,doge]
num_plots = 6
total_cols = 2
total_rows = 3
fig, axs = plt.subplots(nrows=total_rows, ncols=total_cols,
                        figsize=(14*total_cols, 7*total_rows), constrained_layout=True)
for i, var in enumerate(crypto):
    row = i//total_cols
    pos = i % total_cols
    sns.set_context('paper', font_scale = 2)
    plot =  sns.lineplot(data=cryptoDf[i], x="Date", y="Close",color='#732C2C',palette ='coolwarm',ax=axs[row][pos])
    axs[row][pos].set_title(crypto[i])
#成交量線圖可視化
fig, axs = plt.subplots(nrows=total_rows, ncols=total_cols,
                        figsize=(14*total_cols, 7*total_rows), constrained_layout=True)
for i, var in enumerate(crypto):
    row = i//total_cols
    pos = i % total_cols
    sns.set_context('paper', font_scale = 2)
    plot =  sns.lineplot(data=cryptoDf[i], x="Date", y="Volume",color='#732C2C',palette ='coolwarm',ax=axs[row][pos])
    axs[row][pos].set_title(crypto[i])
#百分比線圖可視化
for df in cryptoDf:
    df['Daily Return'] = df['Close'].pct_change()
fig, axs = plt.subplots(nrows=total_rows, ncols=total_cols,
                        figsize=(14*total_cols, 7*total_rows), constrained_layout=True)
for i, var in enumerate(crypto):
    row = i//total_cols
    pos = i % total_cols
    cryptoDf[i]['Daily Return'].plot(ax=axs[row][pos], legend=True,color='#732C2C', linestyle='--', marker='.')
    axs[row][pos].set_title(crypto[i])
    
#直方圖可視化
fig, axs = plt.subplots(nrows=total_rows, ncols=total_cols,
                        figsize=(8*total_cols, 5*total_rows))
for i, var in enumerate(crypto):
    row = i//total_cols
    pos = i % total_cols
    plot =sns.distplot(cryptoDf[i]['Daily Return'], bins=100, color='#732C2C',ax=axs[row][pos])
    axs[row][pos].set_title(crypto[i])
    plt.ylabel('Daily Return')

plt.tight_layout()

#相關性判斷可式化

#散點圖可視化
closeDf18=pd.DataFrame()
closeDf18['btc']=btc18['Close']
closeDf18['eth']=eth18['Close']
closeDf18['bit']=bit18['Close']
returns18 = closeDf18.pct_change()
returns18.head()

btc=equalize(btc,eth)
doge=equalize(doge,eth)
closeDf=pd.DataFrame()
closeDf['btc']=btc['Close']
closeDf['eth']=eth['Close']
closeDf['doge']=doge['Close']
returns = closeDf.pct_change()
returns.head()

sns.jointplot(data=returns18, x='btc', y="bit", kind='scatter',color='#732C2C',height=8)
plt.show()

#熱圖可視化
def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb =matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

hc = ['#F8EDED', '#EAC8C8', '#CF7F7F', '#BA4949', '#732C2C']
th = [0, 0.1, 0.5, 0.9, 1]

cdict = NonLinCdict(th, hc)
cm = LinearSegmentedColormap('test', cdict)
plt.figure(figsize=(10,6))
sns.heatmap(returns18.corr(), annot=True, cmap=cm)
plt.show()

plt.figure(figsize=(10,6))
sns.heatmap(returns.corr(), annot=True, cmap=cm)
plt.show()

#風險回顧可視化
#bitconnect
rets = returns18.dropna()

area = np.pi * 20

plt.figure(figsize=(10, 7))
plt.scatter(rets.mean(), rets.std(), s=area)
plt.xlabel('Expected return')
plt.ylabel('Risk')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom', 
                 arrowprops=dict(arrowstyle='-', color='#732C2C', connectionstyle='arc3,rad=-0.3'))
#degecoin
rets = returns.dropna()

area = np.pi * 20

plt.figure(figsize=(10, 7))
plt.scatter(rets.mean(), rets.std(), s=area)
plt.xlabel('Expected return')
plt.ylabel('Risk')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom', 
                 arrowprops=dict(arrowstyle='-', color='#732C2C', connectionstyle='arc3,rad=-0.3'))
