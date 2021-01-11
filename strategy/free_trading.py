from common.utils.account_db import AccountDb
from common.utils.logger import Logger
from entity.position import Position
from entity.position_info import PositionInfo

log = Logger(__name__).logger


class FreeTrading:
    def __init__(self):
        log.info('---- 自由买卖策略 ----')

    # 创建账号
    @staticmethod
    def create_account(account):
        return AccountDb.save_account(account)

    # 往账号存钱
    @staticmethod
    def save_money(account):
        # 先查询账号, 然后累加余额
        origin_account = AccountDb.query_account(account)
        origin_account.balance = origin_account.balance + account.balance
        return AccountDb.update_account(origin_account)

    # 查询账号总资产(总市值 + 余额)
    @staticmethod
    def query_account_total_market_value(account):
        total_value, _ = FreeTrading.query_market_value_and_positions(account)
        return total_value

    # 查询账号总资产和头寸现价
    @staticmethod
    def query_market_value_and_positions(account):
        origin_account = AccountDb.query_account(account)
        # 股票详情
        positions = origin_account.positions
        # 余额
        position_info_list = []
        total_value = origin_account.balance
        for position in positions:
            stock_code = position.stock_code
            stock_num = position.stock_num
            cost_price = position.stock_price
            trade_date = position.trade_date
            # position info对象
            position_info = PositionInfo(stock_code, stock_num, cost_price, trade_date)
            position_info_list.append(position_info)
            total_value = total_value + position_info.latest_price * stock_num
        return total_value, position_info_list

    # 查询股票现价和股数
    @staticmethod
    def query_account_market_positions(account):
        _, position_info_list = FreeTrading.query_market_value_and_positions(account)
        return position_info_list

    # 查询股票成本和股数
    @staticmethod
    def query_account_positions(account):
        origin_account = AccountDb.query_account(account)
        return origin_account.positions

    # 查询账号余额
    @staticmethod
    def query_account_balance(account):
        origin_account = AccountDb.query_account(account)
        return origin_account.balance

    # 买入股票
    @staticmethod
    def buy_stock(account, position):
        # 校验余额是否足够
        origin_account = AccountDb.query_account(account)
        origin_balance = origin_account.balance
        origin_positions = origin_account.positions
        # 买入股票的数据
        stock_code = position.stock_code
        price = position.stock_price
        num = position.stock_num
        stock_value = price * num
        is_bought = False
        if origin_balance >= stock_value:
            # 修改原账户的余额
            origin_account.balance = origin_balance - stock_value
            # 修改原账号的头寸
            is_modified = False
            for origin_position in origin_positions:
                if origin_position.stock_code == stock_code:
                    tmp_price = origin_position.stock_price
                    tmp_num = origin_position.stock_num
                    # 修改原始账户股数
                    origin_position.stock_num = tmp_num + num
                    # 修改原始账户股价
                    origin_position.stock_price = (stock_value + tmp_price * tmp_num) / (tmp_num + num)
                    is_modified = True
                    break
            # 也有可能原来没买过这个股票, 直接添加
            if not is_modified:
                origin_positions.append(Position(stock_code, num, price, position.trade_date))
            # 修改数据
            is_bought = AccountDb.update_account(origin_account)
        return is_bought

    # 卖出股票
    @staticmethod
    def sell_stock(account, position):
        # 校验头寸是否足够
        origin_account = AccountDb.query_account(account)
        origin_balance = origin_account.balance
        origin_positions = origin_account.positions
        # 卖出股票的数据
        stock_code = position.stock_code
        price = position.stock_price
        num = position.stock_num
        stock_value = price * num
        is_sold = False
        for origin_position in origin_positions:
            # 找到要卖出的股票
            if origin_position.stock_code == stock_code:
                tmp_num = origin_position.stock_num
                if tmp_num >= num:
                    # 修改原始账户股数
                    origin_position.stock_num = tmp_num - num
                    # 余额增加
                    origin_account.balance = origin_balance + stock_value
                    # 修改数据
                    is_sold = AccountDb.update_account(origin_account)
                    break
        # 如果股数为0, 清除这条数据
        FreeTrading.clear_empty_stock(account)
        return is_sold

    # 注销账号
    @staticmethod
    def cancel_account(account):
        return AccountDb.delete_account(account)

    # 查询数据库所有账号
    @staticmethod
    def show_all_accounts_info():
        return AccountDb.query_all()

    # 清除头寸中为0的股票
    @staticmethod
    def clear_empty_stock(account):
        # 如果股数为0, 清除这条数据
        origin_account = AccountDb.query_account(account)
        origin_positions = origin_account.positions
        new_positions = []
        for origin_position in origin_positions:
            if origin_position.stock_num != 0:
                new_positions.append(origin_position)
        origin_account.positions = new_positions
        # 修改数据
        return AccountDb.update_account(origin_account)


if __name__ == '__main__':
    p1 = Position('aaa', 100, 2.8)
    p2 = Position('bbb', 100, 2.8)
    list1 = [p1, p2]
    for it in list1:
        if it.stock_code == 'bbb':
            it.stock_num = 200
            it.stock_price = 5.8
    print('888888888')
    for it in list1:
        print(it.stock_code)
        print(it.stock_price)
        print(it.stock_num)
