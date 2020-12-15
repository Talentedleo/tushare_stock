import os

from common.quotation.data_wrapper import Client
from common.utils.db import ShelvePersistence
from common.utils.logger import Logger
from strategy.turtle_trade import Turtle
from component.filtered_stock.stock_chance import get_capital_inflow_stock_list

log = Logger(__name__).logger


# todo 注意: 2008年, 2015年股灾. 小心2022年
# 使用场景: 慢牛, 牛市, 大盘走势走势好的情况
class TurtleWorkFlow:
    def __init__(self, stock_code='000725.SZ', days=365, balance=100000):
        # 准备工作
        self.stock_code = stock_code
        self.days = days
        self.fields = 'ts_code,trade_date,close,high,low,vol,amount'
        self.cli = Client(self.stock_code, self.days, self.fields)
        # 日数据
        self.stock_df = self.cli.get_stock_df_daily()
        # 海龟策略
        self.turtle = Turtle(balance)

    # 获取前些天的df数据
    def get_earlier_df(self, days=1):
        return self.stock_df[days:]

    @staticmethod
    def check_position():
        # 查询头寸
        ShelvePersistence.positions()

    def check_enter(self, ts_df, threshold=20):
        # 查询买入时机
        enter_flag = self.turtle.check_enter(self.stock_code, ts_df, threshold)
        log.info('enter? {}'.format(enter_flag))
        return enter_flag

    def get_enter_price(self, ts_df, threshold=20):
        # 查询买入时机
        enter_price = self.turtle.get_enter_price(self.stock_code, ts_df, threshold)
        log.info('enter price: {}'.format(enter_price))
        return enter_price

    def check_stop(self, ts_df):
        # 查询止损时机
        with ShelvePersistence.open() as file:
            for key in file:
                code = file[key]['ts_code']
                if code == self.stock_code:
                    # 查询止损时机
                    stop_flag = self.turtle.check_stop(code, ts_df, file[key])
                    log.info('stop? {}'.format(stop_flag))
                    return stop_flag

    def check_exit(self, ts_df, threshold=5):
        # 查询减仓时机
        exit_flag = self.turtle.check_exit(self.stock_code, ts_df, threshold)
        log.info('exit? {}'.format(exit_flag))
        return exit_flag

    def save_buy(self, ts_df):
        # 买入并保存
        result = self.turtle.calc_buy(self.stock_code, ts_df)
        log.info('buy? {}'.format(result))

    def save_sell(self, ts_df, sell_rate=0.8):
        # 卖出并保存
        result = self.turtle.calc_reduce(self.stock_code, ts_df, sell_rate)
        log.info('sale? {}'.format(result))

    def check_cost(self, ts_df):
        cost = self.turtle.check_cost(self.stock_code, ts_df)
        log.info('**目前持仓 {} 的市值是: {}'.format(self.stock_code, cost))
        return cost


def start_invest(stock_code, total_data_day, day_before, balance, enter_threshold, exit_threshold, result_list):
    """
    启动投资的主方法
    :param stock_code: 股票代码
    :param total_data_day: 总时间段内
    :param day_before: n天前的数据
    :param balance: 账户总额
    :param enter_threshold: n天突破就买入
    :param exit_threshold: n天贬值就卖出
    :return:
    """
    wf = TurtleWorkFlow(stock_code, total_data_day, balance)
    day = day_before
    exit_time = 0
    stop_time = 0
    total_profit = 0
    # 模拟最近 day 天, 使用海龟策略的利润情况
    for i in reversed(range(day)):
        log.info('%d 天前的数据', i + 1)
        df = wf.get_earlier_df(i + 1)
        # 买入股票
        if wf.check_enter(df, enter_threshold):
            wf.save_buy(df)
        # 减仓
        if wf.check_exit(df, exit_threshold):
            if exit_time == 0:
                wf.save_sell(df, 0.5)
                exit_time += 1
            elif exit_time == 1:
                # 全部清空
                wf.save_sell(df, 1)
                exit_time = 0
        # 止损
        if wf.check_stop(df):
            if stop_time == 0:
                wf.save_sell(df, 0.5)
                stop_time += 1
            elif stop_time == 1:
                # 全部清空
                wf.save_sell(df, 1)
                stop_time = 0
    wf.check_position()
    # 当前账户持股市值
    now_cost = wf.check_cost(wf.stock_df)
    # 总的账户利润
    if now_cost is not None:
        total_profit = wf.turtle.balance + now_cost - balance
    log.info('账户: {0:0.2f}'.format(wf.turtle.balance))
    result_item = '{0} 战果: {1:0.2f}'.format(stock_code, total_profit)
    result_list.append(result_item)


def remove_positions_db():
    # 删除头寸db, 这里想测试多支股票的实际投资效果, 所以每次临时删除, 实际操作时不需要删除的, 保持账户用来查询
    project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../'
    db_path = os.path.abspath(project_path + '/storage/positions.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    else:
        log.info("---- The file does not exist ----")


def get_multi_stock_enter_price(total_data_day=90, balance=100000, enter_threshold=15):
    # 京东方A '000725.SZ'
    # TCL科技 '000100.SZ'
    # 比亚迪 '002594.SZ'
    # 美的集团 '000333.SZ'
    # 赣锋锂业 '002460.SZ'
    # 格力电器 '000651.SZ'
    # 科大讯飞 '002230.SZ'
    # 海康威视 '002415.SZ'
    # 索菲亚 '002572.SZ'
    # 漫步者 '002351.SZ'
    # 山东黄金 '600547.SH'
    # 兴业证券 '601377.SH'
    # 复星医药 '600194.SH'
    # 福耀玻璃 '600660.SH'
    # 永辉超市 '601933.SH'
    # 中国外运 '601598.SH'
    # 西藏珠峰 '600338.SH'
    stock_list = ['000725.SZ', '000100.SZ', '002594.SZ', '000333.SZ', '002460.SZ', '002230.SZ', '002415.SZ',
                  '002572.SZ',
                  '601377.SH', '600660.SH', '601933.SH', '601598.SH', '600338.SH', '000858.SZ']
    result_list = []
    # 将多支股票放入策略中运算测试
    for code_item in stock_list:
        # 区间突破就买入, 亏损超10%就止损
        wf = TurtleWorkFlow(code_item, total_data_day, balance)
        enter_price = wf.get_enter_price(wf.stock_df, enter_threshold)
        result_item = '{0} 突破价格: {1:0.2f}'.format(code_item, enter_price)
        result_list.append(result_item)
    log.info('*' * 50)
    # 打印总盈亏结果
    for stock_item in result_list:
        log.info(stock_item)


def get_multi_stock_profit(stock_list=[]):
    if not stock_list:
        # 京东方A '000725.SZ'
        # 东山精密 '002384.SZ'
        # 长城汽车 '601633.SH'
        # TCL科技 '000100.SZ'
        # 比亚迪 '002594.SZ'
        # 美的集团 '000333.SZ'
        # 赣锋锂业 '002460.SZ'
        # 科大讯飞 '002230.SZ'
        # 海康威视 '002415.SZ'
        # 福耀玻璃 '600660.SH'
        # 长城汽车 '601633.SH'
        stock_list = ['000725.SZ', '002384.SZ', '601633.SH', '000333.SZ']
    result_list = []
    # 将多支股票放入策略中运算测试
    for code_item in stock_list:
        remove_positions_db()
        # todo 使用场景: 大盘趋势好, 使用基本都赚. 修改买入和卖出 threshold
        # 区间突破就买入, 亏损超10%就止损
        start_invest(code_item, 120, 30, 100000, 15, 10, result_list)
        # start_invest(code_item, 1850, 1825, 100000, 15, 10, result_list)
    log.info('*' * 50)
    # 打印总盈亏结果
    for stock_item in result_list:
        log.info(stock_item)


# 筛选后资金流入的多支股票 进行海龟投资策略
def check_capital_inflow_stock_profit(df_days=120, days_interval=10, target_amount=0):
    money_flow_filtered_list = get_capital_inflow_stock_list(df_days, days_interval, target_amount)
    get_multi_stock_profit(money_flow_filtered_list)


if __name__ == '__main__':
    # todo 总结 筛选后的股票进行海龟交易回测利润

    # 筛选后资金流入的多支股票 进行海龟投资策略
    # check_capital_inflow_stock_profit(60, 20, 70000)

    # 默认的股票 进行海龟投资策略
    get_multi_stock_profit()

    # 多支股票明天的买入预期价位
    # get_multi_stock_enter_price()
