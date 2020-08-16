import common.graph.graph_drawer as graph
from common.quotation.data_filter import Filter
from common.quotation.data_wrapper import Client
import common.quotation.indicator as indicator
from common.utils import yml_loader as config
from common.utils import mapping_util
from strategy import oscillation_zone as strategy
import talib as ta
import time
from common.utils.logger import Logger

log = Logger(__name__).logger

if __name__ == '__main__':
    stock = config.get_value('STOCK')
    stock_code = stock.get('STOCK_CODE')
    # stock_code = '601377.SH'
    # days = stock.get('DAYS_INTERVAL')
    days = 120
    fields = stock.get('FIELDS')

    cli = Client(stock_code, days, fields)
    # 日数据
    stock_df = cli.get_stock_df_daily()
    # 周数据
    # stock_df = cli.get_stock_df_weekly()

    # atr数据
    stock_df = indicator.get_atr_df(stock_df)
    graph.draw_field_compare_plot(stock_df, 'atr', '{} Stock Market'.format(stock_code), 10)

    # sma数据
    # stock_df = indicator.get_sma_df(stock_df)
    # graph.draw_field_compare_plot(stock_df, 'sma', '{} Stock Market'.format(stock_code), 10)

    # 成交量情况
    # graph.draw_default_compare_plot_bar(stock_df, '{} Stock Market'.format(stock_code), 30)

    # 换手率
    # stock_df = cli.get_stock_info_df()
    # graph.draw_field_compare_plot_bar(stock_df, 'turnover_rate', '{} Stock Market'.format(stock_code), 2)

    # 和大盘走势比较
    # 日指数
    # index_df = cli.get_index_df_daily()
    # 周指数
    # index_df = cli.get_index_df_weekly()
    # log.info('---- 绘制股票和指数的比较图 ----')
    # graph.draw_default_compare_plot(stock_df, index_df, '{} week data'.format(stock_code))
