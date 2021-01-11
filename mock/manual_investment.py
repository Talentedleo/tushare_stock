from common.quotation.data_wrapper import Client
from common.utils import yml_loader as config
from common.utils.date_util import calc_bus_day_num, get_now_date
from entity.account import Account
from entity.position import Position
from strategy.free_trading import FreeTrading

fields = config.get_value('DAILY_FIELDS')


# 创建账号
def create_account(name, balance=100000.0):
    FreeTrading.create_account(Account(name, balance))


# 买入
def buy_stock(name, stock_code, stock_num, price=None):
    # 买入价格为None, 默认使用当天开盘价格 x 1.01来模拟买入
    buy_price = generate_mock_open_price(stock_code, price)
    FreeTrading.buy_stock(Account(name), Position(stock_code, stock_num, buy_price))


# 当天开盘价格 x 1.01来得到模拟买入价格
def generate_mock_open_price(stock_code, price=None):
    if price is None:
        # 如果不传价格, 查询最近一天的收盘价格
        cli = Client(stock_code, 7, fields)
        # 因为拿到的数据是倒序的
        stock_price = cli.get_stock_df_daily()['open'].head(1).values[0]
        # 模拟没估计好估价, 买高了
        return float(stock_price) * 1.01
    else:
        return price


# 卖出
def sell_stock(name, stock_code, stock_num, price=None):
    FreeTrading.sell_stock(Account(name), Position(stock_code, stock_num, price))


# 打印账户所有信息
def print_account_info(name):
    market_value, position_info_list = FreeTrading.query_market_value_and_positions(Account(name))
    balance = FreeTrading.query_account_balance(Account(name))
    print('账号 {} 总市值: {:.2f} 余额: {:.2f}'.format(name, market_value, balance))
    for position_info in position_info_list:
        print(
            '股票: {} {} 持仓: {} 成本: {:.2f} 现价: {:.2f} 盈利率: {:.2%} 实际盈亏: {:.2f}   ==>   买入日期: {} 持股天数: {}'.format(
                position_info.stock_code,
                position_info.stock_name,
                position_info.stock_num,
                position_info.cost_price,
                position_info.latest_price,
                position_info.profit_rate,
                position_info.profit,
                position_info.trade_date,
                calc_bus_day_num(position_info.trade_date, get_now_date())))


# 查看所有账号和头寸成本
def show_all_accounts():
    account_list = FreeTrading.show_all_accounts_info()
    for account in account_list:
        print(account)


if __name__ == '__main__':
    # 京东方A '000725.SZ'
    # 长城汽车 '601633.SH'
    # 美的集团 '000333.SZ'
    # TCL科技 '000100.SZ'
    # 比亚迪 '002594.SZ'
    # 华友钴业 '603799.SH'

    # 创建账号
    # create_account('t_mock', 45390.98)
    # create_account('t_real', 45390.98)
    # 所有账号
    # show_all_accounts()
    # 账号信息
    # 测试账号
    # print_account_info('t_mock')
    # 实际账号
    print_account_info('t_real')
    # 买入
    # buy_stock('t_mock', '601360.SH', 100)
    # buy_stock('t_real', '603087.SH', 100)
    # 卖出
    # sell_stock('t_mock', '000725.SZ', 2000)
    # sell_stock('t_real', '603087.SH', 100)
