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
df.timestamp = pd.to_datetime(df.timestamp, unit='ms')

lastAuth = 0
notnull = df[(df.timestamp >= '2020-11-21 14:00:00') & (df.timestamp < '2022-01-01 14:00:00')]
for index, row in notnull.iterrows():
    rowplus = df.iloc[index+1]
    if row['close'] > rowplus['close']:
        result = row['close'] - rowplus['close']
        print(row['close'], " - " ,rowplus['close'], " = ", result)
        if lastAuth < result:
            lastAuth = result

print(lastAuth)