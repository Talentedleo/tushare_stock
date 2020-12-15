import common.graph.graph_drawer as graph
import common.quotation.indicator as indicator
from common.quotation.data_wrapper import Client
from common.utils.logger import Logger
import component.filtered_stock.stock_chance as chance

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


# 绘制 单个 图形
def draw_multi_graph_by_stock(stock):
    drawer = DrawComponent(stock, 120)

    drawer.get_atr_graph(5)
    #################################################
    # drawer.get_money_flow_graph(5)
    #################################################
    # drawer.get_turnover_graph(5)
    #################################################
    # drawer.get_amount_graph()
    #################################################
    # drawer.get_sma_graph()
    #################################################
    # drawer.get_index_compare_graph()


# 绘制 多个 图形
def draw_multi_graph_by_stock_list(stock_list):
    for stock in stock_list:
        draw_multi_graph_by_stock(stock)


# 绘制 沪深股通十大成交股 的图形
def draw_multi_graph_by_top10_company():
    top10_company_df = chance.get_top10_company()
    for company in top10_company_df['ts_code']:
        draw_multi_graph_by_stock(company)


if __name__ == '__main__':
    # todo 总结 选股后画图再次分析

    # 京东方A '000725.SZ'
    # 长城汽车 '601633.SH'
    # 美的集团 '000333.SZ'
    # TCL科技 '000100.SZ'
    # 比亚迪 '002594.SZ'

    # 东山精密 '002384.SZ'
    # 神州数码 '000034.SZ'
    # 安宁股份 '002978.SZ'
    # 桐昆股份 '601233.SH'
    # 赣锋锂业 '002460.SZ'
    # 隆基股份 '601012.SH'
    # 分众传媒 '002027.SZ'

    # 绘制 单个 股票图形
    # draw_multi_graph_by_stock('000725.SZ')

    # 绘制 多个 股票图形
    # draw_multi_graph_by_stock_list(['000725.SZ', '601633.SH'])

    # 绘制 沪深股通十大成交股 的图形
    draw_multi_graph_by_top10_company()
