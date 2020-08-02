import talib as ta


def get_atr_df(df, period=14):
    df['atr'] = ta.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=period)
    return df


def get_sma_df(df, period=5):
    df['sma'] = ta.SMA(df['close'].values, timeperiod=period)
    return df
