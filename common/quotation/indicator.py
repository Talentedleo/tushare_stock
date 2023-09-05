# import talib as ta
#
# from common.utils.logger import Logger
#
# log = Logger(__name__).logger
#
#
# def get_atr_df(df, period=14):
#     log.info('---- 生成atr数据 ----')
#     # 计算最新的atr数据需要将数据翻转一下, copy()一下使用, 防止警告
#     df = df[::-1].copy()
#     df['atr'] = ta.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=period)
#     # 翻转回来是为了绘图用
#     df = df[::-1]
#     return df
#
#
# def get_sma_df(df, period=5):
#     log.info('---- 生成sma数据 ----')
#     df['sma'] = ta.SMA(df['close'].values, timeperiod=period)
#     return df
