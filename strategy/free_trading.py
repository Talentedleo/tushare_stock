from common.utils.db import ShelvePersistence
from common.utils.logger import Logger

log = Logger(__name__).logger


class FreeTrading:
    def __init__(self):
        log.info('---- 自由买卖策略 ----')
        # 实例化的时候从数据库读取账号余额

    # 创建账号
    def create_account(self):
        pass

    # 查询账号总市值
    def query_account_total_market_value(self):
        pass

    # 查询股票头寸
    def query_account_positions(self):
        pass

    # 查询账号余额
    def query_account_balance(self):
        pass

    # 买入股票
    def buy_stock(self):
        pass

    # 卖出股票
    def sell_stock(self):
        pass

    # 注销账号
    def cancel_account(self):
        pass
