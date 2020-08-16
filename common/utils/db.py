import os
import shelve

import common.utils.tool as tool

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

    # obj格式：{'positions': positions, 'cost': cost}
    # 参数：
    #   positions持仓，格式[{bought_price1, bought_amount}, {bought_price2, bought_amount}..{bought_price4, bought_amount}]
    #   cost: 持仓总成本
    def save(self, ts_code, last_close, position_size):
        stock = ts_code[0]
        new_position = (last_close, position_size)
        new_cost = position_size * 100 * last_close

        old_data = self.load(stock)
        # 创建文件夹
        tool.create_dir(base_dir)
        shelve_file = shelve.open(base_dir + "/positions")

        if old_data is None:
            shelve_file[stock] = {'ts_code': ts_code, 'positions': [new_position], 'cost': new_cost}
            shelve_file.close()
            return True
        else:
            positions = old_data['positions']
            if len(positions) < 4:
                positions.append(new_position)
                cost = old_data['cost'] + new_cost
                shelve_file[stock] = {'ts_code': ts_code, 'positions': positions, 'cost': cost}
                shelve_file.close()
                return True
            else:
                return False

    @staticmethod
    def positions():
        shelve_file = shelve.open(base_dir + "/positions")
        for key in shelve_file:
            print(key, shelve_file[key])
