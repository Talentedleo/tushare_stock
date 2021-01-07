import common.graph.graph_drawer as graph
import common.quotation.indicator as indicator
from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config
from common.utils.logger import Logger

log = Logger(__name__).logger
fields = config.get_value('DAILY_FIELDS')


class DrawComponent:
    def __init__(self, stock_code, day):
        # 准备工作
        self.stock_code = stock_code
        # stock_code = '601377.SH'
        self.days = day
        self.fields = fields
        self.cli = Client(self.stock_code, self.days, self.fields)
        # 日数据
        self.stock_df = self.cli.get_stock_df_daily()
        # 周数据
        # self.stock_df = cli.get_stock_df_weekly()

    def get_atr_graph(self, step=10):
        # atr数据
        self.stock_df = indicator.get_atr_df(self.stock_df, 14)
        graph.draw_field_compare_plot(self.stock_df, 'atr', '{} Stock Market'.format(self.stock_code), step)

    def get_sma_graph(self, step=10):
        # sma数据
        self.stock_df = indicator.get_sma_df(self.stock_df)
        graph.draw_field_compare_plot(self.stock_df, 'sma', '{} Stock Market'.format(self.stock_code), step)

    def get_amount_graph(self, step=30):
        # 成交量情况
        graph.draw_default_compare_plot_bar(self.stock_df, '{} Stock Market'.format(self.stock_code), step)

    def get_turnover_graph(self, step=10):
        # 换手率
        self.stock_df = self.cli.get_stock_info_df()
        graph.draw_field_compare_plot_bar(self.stock_df, 'turnover_rate', '{} Stock Market'.format(self.stock_code),
                                          step)

    def get_money_flow_graph(self, step=10):
        # 每日收盘价 和 个股资金流向
        money_flow_df = self.cli.get_money_flow_df()
        money_flow_df['close'] = self.stock_df['close']
        graph.draw_field_compare_plot_bar(money_flow_df, 'net_mf_amount', '{} Stock Market'.format(self.stock_code),
                                          step)

    def get_accumulative_money_flow_graph(self, step=10):
        # 累加资金流向
        money_flow_df = self.cli.get_money_flow_df()
        money_flow_df['close'] = self.stock_df['close']
        money_flow_df = money_flow_df[::-1]
        money_flow_df['total_net'] = money_flow_df['net_mf_amount'].cumsum(axis=0)
        money_flow_df = money_flow_df[::-1]
        graph.draw_field_compare_plot_bar(money_flow_df, 'total_net', '{} Stock Market'.format(self.stock_code),
                                          step)

    def get_index_compare_graph(self):
        # 和大盘走势比较
        # 日指数
        index_df = self.cli.get_index_df_daily()
        # 周指数
        # index_df = cli.get_index_df_weekly()
        log.info('---- 绘制股票和指数的比较图 ----')
        graph.draw_default_compare_plot(self.stock_df, index_df, '{} week data'.format(self.stock_code))
