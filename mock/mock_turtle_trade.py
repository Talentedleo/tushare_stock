from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config
from strategy.turtle_trade import Turtle
from common.utils.db import ShelvePersistence
if __name__ == '__main__':
    # 准备工作
    stock = config.get_value('STOCK')
    stock_code = stock.get('STOCK_CODE')
    # stock_code = '601377.SH'
    days = 120
    fields = stock.get('FIELDS')
    cli = Client(stock_code, days, fields)
    # 日数据
    stock_df = cli.get_stock_df_daily()

    #################################################
    # 海龟策略
    turtle = Turtle()
    # enter_flag = turtle.check_enter(stock_code, stock_df)
    # print('enter? {}'.format(enter_flag))

    # 这里存到db的就是所有持仓股票情况
    t_shelve = ShelvePersistence()
    file = t_shelve.open()
    for key in file:
        ts_code = file[key]['ts_code']
        stop_flag = turtle.check_stop(ts_code, stock_df, file[key])
        print('stop? {}'.format(stop_flag))
    file.close()

    # exit_flag = turtle.check_exit(stock_code, stock_df)
    # print('exit? {}'.format(exit_flag))
    # result = turtle.calculate(stock_code, stock_df)
    # print('calc? {}'.format(result))
