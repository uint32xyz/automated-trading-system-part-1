import pandas as pd
import ta

def apply_indicators(group):
    # Calculate RSI
    group['RSI'] = ta.momentum.rsi(group['price'])

    # Calculate SMA
    group['sma_5'] = group['price'].rolling(window=5).mean()
    group['sma_10'] = group['price'].rolling(window=10).mean()
    group['sma_20'] = group['price'].rolling(window=20).mean()
    
    # pvt
    group['price_change_pct'] = group['price'].pct_change()

    # Calculate the term to be added to PVT: Volume times price change percentage
    group['delta_pvt'] = group['volume'] * group['price_change_pct']

    # Calculate cumulative PVT
    group['pvt'] = group['delta_pvt'].cumsum()

    # Calculate MACD
    macd = ta.trend.MACD(group['price'])
    group['MACD'] = macd.macd()
    group['MACD_signal'] = macd.macd_signal()
    
    # Calculate EMA
    group['EMA_9'] = ta.trend.ema_indicator(group['price'], window=9)
    group['EMA_21'] = ta.trend.ema_indicator(group['price'], window=21)
    
    # Calculate Bollinger Bands
    bollinger = ta.volatility.BollingerBands(group['price'])
    group['bollinger_hband'] = bollinger.bollinger_hband()
    group['bollinger_lband'] = bollinger.bollinger_lband()

    # Calculate OBV
    group['OBV'] = ta.volume.on_balance_volume(group['price'], group['volume'])

    # Calculate VPT
    group['VPT'] = ta.volume.volume_price_trend(group['price'], group['volume']).fillna(0)

    group['VWRSI'] = calculate_vwrsi(group)
    
    return group

def calculate_vwrsi(data, period=14):
    # Calculate price changes
    delta = data['price'].diff()
    
    # Adjust gains and losses by volume
    volume_weighted = delta * data['volume']
    gain = (volume_weighted.where(volume_weighted > 0, 0)).rolling(window=period).mean()
    loss = (-volume_weighted.where(volume_weighted < 0, 0)).rolling(window=period).mean()

    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

df = pd.read_csv('data/raw_data.csv')
df.sort_values(by=['symbol', 'name', 'timestamp'], inplace=True)
df = df.groupby('symbol').apply(apply_indicators)
df.dropna(inplace=True)
df.to_csv('data/processed_data.csv', index=False)
