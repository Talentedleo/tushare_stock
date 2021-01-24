import os
import shelve

import common.utils.tool as tool
from Exception.object_error import ObjectError
from common.utils.logger import Logger

log = Logger(__name__).logger
# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../../'
base_dir = os.path.abspath(project_path + '/storage')


class AllDataDb:
    @staticmethod
    def open():
        return shelve.open(base_dir + "/all_data")

    # 根据key查询数据
    @staticmethod
    def query_obj(key):
        """
        根据key查询数据
        :param key: 键
        :return: value 对象或者字典
        """
        shelve_file = None
        result_dict = None
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AllDataDb.open()
            if key in shelve_file:
                result_dict = shelve_file[key]
        finally:
            shelve_file.close()
        return result_dict

    # 保存key-value数据
    @staticmethod
    def save_obj(key, value):
        """
        保存key-value数据
        :param key: 键
        :param value: 值, 放一个对象或者字典, eg: {'balance': account.balance, 'positions': account.positions}
        :return: bool
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AllDataDb.open()
            shelve_file[key] = value
            shelve_file.close()
            return True
        except ObjectError:
            return False

    # 根据key删除数据
    @staticmethod
    def delete_obj(key):
        """
        根据key删除数据
        :param key: 键
        :return: bool
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AllDataDb.open()
            del shelve_file[key]
            shelve_file.close()
            return True
        except ObjectError:
            return False


if __name__ == '__main__':
    pass
