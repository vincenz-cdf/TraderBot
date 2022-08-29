%matplotlib inline
import matplotlib.pyplot as plt
from binance.client import Client
import pandas as pd
import time
from math import *
import numpy as np

client = Client()
klinesT = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "01 january 2020")

df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])

del df['ignore']
del df['close_time']
del df['quote_av']
del df['trades']
del df['tb_base_av']
del df['tb_quote_av']

df = df.set_index(df['timestamp'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['timestamp']

usdt = 100
coin = 0
wallet = 0
fee = 0.0007
lastAth = 0
lastIndex = df.first_valid_index()
purchasePrice_array = [99999.0]
increaseCryptoRef = 400.0
decreaseCryptoRef = -10.0

print("départ : ",usdt," USDT")

dt = None
dt = pd.DataFrame(columns = ['date','position', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

for index, row in df.iterrows():
    if(row['close'] < purchasePrice_array[-1]+decreaseCryptoRef and usdt > 5):
        coin = usdt / row['close']
        frais = fee * coin
        coin = coin - frais
        usdt = 0
        wallet = coin * row['close']
        purchasePrice_array.append(row['close'])
        myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': frais * row['close'],'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/1}
        dt = dt.append(myrow,ignore_index=True)
    
    if(row['close'] > purchasePrice_array[-1]+increaseCryptoRef and coin > 0):
        usdt = coin * row['close']
        frais = fee * usdt
        usdt = usdt - frais
        coin = 0
        wallet = usdt
        purchasePrice_array.append(row['close'])
        myrow = {'date': index,'position': "Sell",'price': row['close'],'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/1}
        dt = dt.append(myrow,ignore_index=True)
    
string = "Stratégies de tradings"
figure = plt.figure(figsize=(20, 6), dpi=80)
plt.title(string)

usdt = 100
coin = 0
wallet = 0
fee = 0.0007
lastAth = 0
lastIndex = df.first_valid_index()
purchasePrice_array = [99999.0]
increaseCryptoRef = 400.0
decreaseCryptoRef = -10.5
dt2 = None
dt2 = pd.DataFrame(columns = ['date','position', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

for index, row in df.iterrows():
    if(row['close'] < purchasePrice_array[-1]+decreaseCryptoRef and usdt > 5):
        coin = usdt / row['close']
        frais = fee * coin
        coin = coin - frais
        usdt = 0
        wallet = coin * row['close']
        purchasePrice_array.append(row['close'])
        myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': frais * row['close'],'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/1}
        dt2 = dt2.append(myrow,ignore_index=True)
    
    if(row['close'] > purchasePrice_array[-1]+increaseCryptoRef and coin > 0):
        usdt = coin * row['close']
        frais = fee * usdt
        usdt = usdt - frais
        coin = 0
        wallet = usdt
        purchasePrice_array.append(row['close'])
        myrow = {'date': index,'position': "Sell",'price': row['close'],'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/1}
        dt2 = dt2.append(myrow,ignore_index=True)
    
plot1 = plt.plot(dt['date'], dt['wallet'], color="green", linestyle="dashed", label="-10/400")
plot2 = plt.plot(dt2['date'], dt2['wallet'], color="blue", linestyle="solid", label="-20/400")
plt.legend(loc="upper left")
ax = plt.axes()
ax = ax.set(xlabel="Date",ylabel="Quantité USDT")