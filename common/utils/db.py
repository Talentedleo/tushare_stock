import math
import os
import shelve

import common.utils.tool as tool
from common.utils.logger import Logger

log = Logger(__name__).logger
# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../../'
base_dir = os.path.abspath(project_path + '/storage')


class ShelvePersistence:
    """
    Shelve为DBM和Pickle的结合，以键值对的方式把复杂对象序列化到文件持久化或者缓存持久化
    """

    @staticmethod
    def open():
        return shelve.open(base_dir + "/positions")

    @staticmethod
    def load(key):
        try:
            shelve_file = shelve.open(base_dir + "/positions")
            if key in shelve_file:
                result = shelve_file[key]
            else:
                result = None
        finally:
            shelve_file.close()
        return result

    # 保存买入
    # obj格式：{'ts_code': ts_code, 'positions': positions, 'cost': cost}
    # 参数：
    #   ts_code: 股票代码
    #   positions: 持仓，格式[{bought_price1, bought_amount}, {bought_price2, bought_amount}..{bought_price4, bought_amount}]
    #   cost: 持仓总成本
    def save_buy(self, ts_code, last_close, position_size):
        """
        保存买入股票
        :param ts_code:
        :param last_close:
        :param position_size:
        :return:
        """
        new_position = (last_close, position_size)
        new_cost = position_size * 100 * last_close

        old_data = self.load(ts_code)
        # 创建文件夹
        tool.create_dir(base_dir)
        shelve_file = self.open()

        if old_data is None:
            shelve_file[ts_code] = {'ts_code': ts_code, 'positions': [new_position], 'cost': new_cost}
            shelve_file.close()
            return True
        else:
            positions = old_data['positions']
            if len(positions) <= 1000:
                positions.append(new_position)
                cost = old_data['cost'] + new_cost
                shelve_file[ts_code] = {'ts_code': ts_code, 'positions': positions, 'cost': cost}
                shelve_file.close()
                return True
            else:
                log.info('请考虑是否买入太频繁?')
                return False

    # 保存卖出
    # obj格式：{'ts_code': ts_code, 'positions': positions, 'cost': cost}
    # 参数：
    #   ts_code: 股票代码
    #   positions: 持仓，格式[{bought_price1, bought_amount}, {bought_price2, bought_amount}..{bought_price4, bought_amount}]
    #   cost: 持仓总成本
    def save_reduce(self, ts_code, last_close, position_rate):
        """
        保存卖出股票
        :param ts_code: 股票代码
        :param last_close: 卖出时的价格
        :param position_rate: 卖出的比例
        :return:
        """
        old_data = self.load(ts_code)
        # 创建文件夹
        tool.create_dir(base_dir)
        shelve_file = self.open()

        # 先查询原来对应股票持仓
        if old_data is None:
            log.error('没有 %s 股票的持仓信息', ts_code)
            return False, 0
        else:
            # 总成本
            old_cost = old_data['cost']
            # 头寸列表
            positions = old_data['positions']
            # 有头寸数据的情况
            if len(positions) > 0:
                # 计算总共有几手股票
                total_size = 0
                for position_tuple in positions:
                    size = position_tuple[1]
                    total_size += size
                # 卖出的数量不能大于原有的数量
                if position_rate <= 1:
                    position_size = math.ceil(position_rate * total_size)
                    # 剩余头寸 = 现头寸 - 减仓头寸
                    record_size = total_size - position_size
                    # 计算成本单价
                    record_price = old_cost / (total_size * 100)
                    # 成本总价
                    record_total = record_price * record_size * 100
                    # 保存数据库
                    record_position = (last_close, record_size)
                    if position_rate != 1:
                        shelve_file[ts_code] = {'ts_code': ts_code, 'positions': [record_position],
                                                'cost': record_total}
                    else:
                        # 全部卖出的情况
                        shelve_file[ts_code] = {'ts_code': ts_code, 'positions': [], 'cost': 0}
                    shelve_file.close()
                    # 计算利润
                    profit = (last_close - record_price) * position_size * 100
                    log.info('**注意: %s 股票被 %0.2f 卖出 %d 手, 盈亏: %0.2f', ts_code, last_close, position_size, profit)
                    return True, last_close * position_size * 100
            else:
                log.info('%s 股票已经清空', ts_code)
                return False, 0

    @staticmethod
    def positions():
        log.info('股票代码, 持仓总成本, 持仓')
        with shelve.open(base_dir + "/positions") as file:
            for key in file:
                ts_code = file[key]['ts_code']
                cost = file[key]['cost']
                positions = file[key]['positions']
                log.info('{}, {}, {}'.format(ts_code, cost, positions))

    @staticmethod
    def check_profit(ts_code, last_close):
        with shelve.open(base_dir + "/positions") as file:
            for key in file:
                code = file[key]['ts_code']
                if code == ts_code:
                    positions = file[key]['positions']
                    total_profit = 0
                    for item in positions:
                        price = item[0]
                        amount = item[1]
                        total_profit += (last_close - price) * amount * 100
                    log.info('{}, profit: {}'.format(code, total_profit))
                    return total_profit
