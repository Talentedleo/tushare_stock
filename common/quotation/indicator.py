import talib as ta


def get_atr_df(df, period=14):
    print('---- 生成atr数据 ----')
    df['atr'] = ta.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=period)
    return df


def get_sma_df(df, period=5):
    print('---- 生成sma数据 ----')
    df['sma'] = ta.SMA(df['close'].values, timeperiod=period)
    return df


