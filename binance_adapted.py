import pandas as pd
import time
import json
import pickle
from math import floor
from email.message import EmailMessage
import ssl
import smtplib
from binance.client import Client

accountName = 'TraderBot'
pairSymbol = 'ETHUSDT' # note the different format for pair symbol on Binance
fiatSymbol = 'USDT'
cryptoSymbol = 'ETH'
myTruncate = 3
# open a pickle file
filename = 'tradedata.pk'

client = Client() # Note that the import for Binance's Client has not been done here

#with open(filename, 'rb') as fi:
#    purchasePrice_array = pickle.load(fi)

data = client.get_klines(symbol=pairSymbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=1000)
df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])

def getBalance(myclient, coin):
    jsonBalance = myclient.get_account()['balances']
    if jsonBalance == []: 
        return 0
    pandaBalance = pd.DataFrame(jsonBalance)
    if pandaBalance.loc[pandaBalance['asset'] == coin].empty: 
        return 0
    else: 
        return float(pandaBalance.loc[pandaBalance['asset'] == coin]['free'])
    
def truncate(n, decimals=0):
    r = floor(float(n)*10**decimals)/10**decimals
    return str(r)

purchasePrice_array=[99999] #a retirer

fiatAmount = getBalance(client, fiatSymbol)
cryptoAmount = getBalance(client, cryptoSymbol)
actualPrice = float(df['close'].iloc[-1])
minToken = 5/actualPrice

print(actualPrice)

if actualPrice < purchasePrice_array[-1]-9.0 :
    if float(fiatAmount) > 5:
        quantityBuy = truncate(float(fiatAmount)/actualPrice, myTruncate)
        purchasePrice = actualPrice
        purchasePrice_array.append(purchasePrice)
        buyOrder = client.place_order(
            symbol=pairSymbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantityBuy)
    print("BUY", buyOrder)
    else:
        print("If you  give me more USD I will buy more",cryptoSymbol)
elif actualPrice > purchasePrice_array[-1]+300.0:
    if float(cryptoAmount) > minToken:
        purchasePrice = actualPrice
        purchasePrice_array.append(purchasePrice)
        sellOrder = client.order_market_sell(
            symbol=pairSymbol,
            quantity=truncate(cryptoAmount, myTruncate))
        print("SELL", sellOrder)
    else:
        print("If you give me more",cryptoSymbol,"I will sell it")
else :
      print("No opportunity to take")
        
with open(filename, 'wb') as fi:
    # dump your data into the file
    pickle.dump(purchasePrice_array, fi)
