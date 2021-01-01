from entity.account import Account
from entity.position import Position
from strategy.free_trading import FreeTrading


# 创建账号
def create_account(name, balance=100000.0):
    FreeTrading.create_account(Account(name, balance))


# 买入
def buy_stock(name, stock_code, stock_num, price=None):
    FreeTrading.buy_stock(Account(name), Position(stock_code, stock_num, price))


# 卖出
def sell_stock(name, stock_code, stock_num, price=None):
    FreeTrading.sell_stock(Account(name), Position(stock_code, stock_num, price))


# 打印账户所有信息
def print_account_info(name):
    market_value, position_info_list = FreeTrading.query_market_value_and_positions(Account(name))
    print('账号 {} 总市值: {}'.format(name, market_value))
    for position_info in position_info_list:
        print(
            '股票: {} {} 持仓: {} 成本: {} 现价: {} 盈利率: {:.2%} 实际盈亏: {:.2f}'.format(position_info.stock_code,
                                                                             position_info.stock_name,
                                                                             position_info.stock_num,
                                                                             position_info.cost_price,
                                                                             position_info.latest_price,
                                                                             position_info.profit_rate,
                                                                             position_info.profit))


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
    # 东山精密 '002384.SZ'
    # 赣锋锂业 '002460.SZ'
    # 隆基股份 '601012.SH'
    # 分众传媒 '002027.SZ'

    # 创建账号
    # create_account('t_20201230', 45390.98)
    # 所有账号
    # show_all_accounts()
    # 账号信息
    print_account_info('t_20201230')
    # 买入
    # buy_stock('t_20201230', '000725.SZ', 2000, 5.80)
    # 卖出
    # sell_stock('t_20201230', '000725.SZ', 2000)
