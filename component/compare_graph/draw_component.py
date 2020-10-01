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


class DrawComponent:
    def __init__(self, stock_code, day):
        # 准备工作
        self.stock_code = stock_code
        # stock_code = '601377.SH'
        self.days = day
        self.fields = 'ts_code,trade_date,close,high,low,vol,amount'
        self.cli = Client(self.stock_code, self.days, self.fields)
        # 日数据
        self.stock_df = self.cli.get_stock_df_daily()
        # 周数据
        # self.stock_df = cli.get_stock_df_weekly()

    def get_atr_graph(self):
        # atr数据
        self.stock_df = indicator.get_atr_df(self.stock_df, 14)
        graph.draw_field_compare_plot(self.stock_df, 'atr', '{} Stock Market'.format(self.stock_code), 10)

    def get_sma_graph(self):
        # sma数据
        self.stock_df = indicator.get_sma_df(self.stock_df)
        graph.draw_field_compare_plot(self.stock_df, 'sma', '{} Stock Market'.format(self.stock_code), 10)

    def get_amount_graph(self):
        # 成交量情况
        graph.draw_default_compare_plot_bar(self.stock_df, '{} Stock Market'.format(self.stock_code), 30)

    def get_turnover_graph(self):
        # 换手率
        self.stock_df = self.cli.get_stock_info_df()
        graph.draw_field_compare_plot_bar(self.stock_df, 'turnover_rate', '{} Stock Market'.format(self.stock_code), 2)

    def get_index_compare_graph(self):
        # 和大盘走势比较
        # 日指数
        index_df = self.cli.get_index_df_daily()
        # 周指数
        # index_df = cli.get_index_df_weekly()
        log.info('---- 绘制股票和指数的比较图 ----')
        graph.draw_default_compare_plot(self.stock_df, index_df, '{} week data'.format(self.stock_code))


if __name__ == '__main__':
    # drawer = DrawComponent('000725.SZ', 120)
    drawer = DrawComponent('002594.SZ', 120)
    drawer.get_atr_graph()
    #################################################
    # drawer.get_sma_graph()
    #################################################
    # drawer.get_amount_graph()
    #################################################
    # drawer.get_turnover_graph()
    #################################################
    # drawer.get_index_compare_graph()
