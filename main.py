import ftx
import pandas as pd
import time
import json
import pickle
from math import *

accountName = ''
pairSymbol = 'ETH/USDT'
fiatSymbol = 'USDT'
cryptoSymbol = 'ETH'
myTruncate = 3
# open a pickle file
filename = 'tradedata.pk'

client = ftx.FtxClient(api_key='',
                   api_secret='', subaccount_name=accountName)

#with open(filename, 'rb') as fi:
#    purchasePrice_array = pickle.load(fi)

data = client.get_historical_data(
    market_name=pairSymbol, 
    resolution=3600, 
    limit=1000, 
    start_time=float(
    round(time.time()))-100*3600, 
    end_time=float(round(time.time())))
df = pd.DataFrame(data)

def getBalance(myclient, coin):
    jsonBalance = myclient.get_balances()
    if jsonBalance == []: 
        return 0
    pandaBalance = pd.DataFrame(jsonBalance)
    if pandaBalance.loc[pandaBalance['coin'] == coin].empty: 
        return 0
    else: 
        return float(pandaBalance.loc[pandaBalance['coin'] == coin]['total'])
    
def truncate(n, decimals=0):
    r = floor(float(n)*10**decimals)/10**decimals
    return str(r)

purchasePrice_array=[99999] #a retirer

fiatAmount = getBalance(client, fiatSymbol)
cryptoAmount = getBalance(client, cryptoSymbol)
actualPrice = df['close'].iloc[-1]
minToken = 5/actualPrice
print(cryptoSymbol ,'price :', actualPrice, fiatSymbol ,'balance', fiatAmount , cryptoSymbol ,'balance :',cryptoAmount)
    
if actualPrice < purchasePrice_array[-1]-300.0 :
    if float(fiatAmount) > 5:
        quantityBuy = truncate(float(fiatAmount)/actualPrice, myTruncate)
        purchasePrice = actualPrice
        purchasePrice_array.append(purchasePrice)
        buyOrder = client.place_order(
            market=pairSymbol, 
            side="buy", 
            price=None, 
            size=quantityBuy, 
            type='market')
        print("BUY", buyOrder)
    else:
        print("If you  give me more USD I will buy more",cryptoSymbol)
elif actualPrice > purchasePrice_array[-1]+300.0:
    if float(cryptoAmount) > minToken:
        purchasePrice = actualPrice
        purchasePrice_array.append(purchasePrice)
        sellOrder = client.place_order(
            market=pairSymbol, 
            side="sell", 
            price=None, 
            size=truncate(cryptoAmount, myTruncate), 
            type='market')
        print("SELL", sellOrder)
    else:
        print("If you give me more",cryptoSymbol,"I will sell it")
else :
      print("No opportunity to take")
        
with open(filename, 'wb') as fi:
    # dump your data into the file
    pickle.dump(purchasePrice_array, fi)