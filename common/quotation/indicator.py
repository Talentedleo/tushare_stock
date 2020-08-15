import talib as ta

from common.utils.logger import Logger

log = Logger(__name__).logger


def get_atr_df(df, period=14):
    log.info('---- 生成atr数据 ----')
    df['atr'] = ta.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=period)
    return df


def get_sma_df(df, period=5):
    log.info('---- 生成sma数据 ----')
    df['sma'] = ta.SMA(df['close'].values, timeperiod=period)
    return df
