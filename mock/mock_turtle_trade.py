from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config
from strategy.turtle_trade import Turtle
from common.utils.db import ShelvePersistence
from common.utils.logger import Logger

log = Logger(__name__).logger

if __name__ == '__main__':
    # 准备工作
    stock = config.get_value('STOCK')
    stock_code = stock.get('STOCK_CODE')
    # stock_code = '601377.SH'
    days = 90
    fields = stock.get('FIELDS')
    cli = Client(stock_code, days, fields)
    # 日数据
    stock_df = cli.get_stock_df_daily()

    #################################################

    # 海龟策略
    turtle = Turtle()

    # 查询头寸
    ShelvePersistence.positions()

    # 查询买入时机
    # enter_flag = turtle.check_enter(stock_code, stock_df)
    # log.info('enter? {}'.format(enter_flag))

    # 这里存到db的就是所有持仓股票情况
    # with ShelvePersistence.open() as file:
    #     for key in file:
    #         ts_code = file[key]['ts_code']
    #         # todo 查询减仓时机
    #         stop_flag = turtle.check_stop(ts_code, stock_df, file[key])
    #         log.info('stop? {}'.format(stop_flag))

    # 查询止损时机
    # exit_flag = turtle.check_exit(stock_code, stock_df)
    # log.info('exit? {}'.format(exit_flag))

    # 买入并保存
    # result = turtle.calc_buy(stock_code, stock_df)
    # log.info('calc? {}'.format(result))

    # 卖出并保存
    # result = turtle.calc_reduce(stock_code, stock_df)
    # log.info('sale? {}'.format(result))

