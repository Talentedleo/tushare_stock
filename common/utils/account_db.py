import math
import os
import shelve

import common.utils.tool as tool
from Exception.object_error import ObjectError
from common.utils.logger import Logger
from entity.account import Account
from entity.position import Position

log = Logger(__name__).logger
# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../../'
base_dir = os.path.abspath(project_path + '/storage')


class AccountDb:
    @staticmethod
    def open():
        return shelve.open(base_dir + "/accounts")

    # 查询所有账号
    @staticmethod
    def query_all():
        """
        查询所有账号
        :return:
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AccountDb.open()
            account_list = []
            for account_name in shelve_file:
                tmp_account = shelve_file[account_name]
                # # 封装account对象
                account = Account(account_name, tmp_account['balance'], tmp_account['positions'])
                account_list.append(account)
        finally:
            shelve_file.close()
        return account_list

    # 查询账号
    @staticmethod
    def query_account(account):
        """
        查询账号
        :param account: 账号对象
        :return:
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            account_name = account.account_name
            shelve_file = AccountDb.open()
            if account_name in shelve_file:
                result = shelve_file[account_name]
                # 封装account对象
                exist_account = Account(account_name, result['balance'], result['positions'])
            else:
                exist_account = None
        finally:
            shelve_file.close()
        return exist_account

    # 保存账号
    @staticmethod
    def save_account(account):
        """
        保存账号
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AccountDb.open()

            account_name = account.account_name
            # 先查询是否有该账号, 如果有, 抛出异常
            if AccountDb.query_account(Account(account_name)) is not None:
                raise ObjectError('Object is already existing!')
            shelve_file[account_name] = {'balance': account.balance, 'positions': account.positions}
            shelve_file.close()
            return True
        except ObjectError:
            return False

    # 修改账号
    @staticmethod
    def update_account(account):
        """
        修改账号
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AccountDb.open()

            account_name = account.account_name
            # 先查询是否有该账号, 如果有, 抛出异常
            exist_account = AccountDb.query_account(Account(account_name))
            if exist_account is None:
                raise ObjectError('Object is None!')
            balance = account.balance
            positions = account.positions
            shelve_file[account_name] = {'balance': balance, 'positions': positions}
            shelve_file.close()
            return True
        except ObjectError:
            return False

    # 删除账号
    @staticmethod
    def delete_account(account):
        """
        删除账号
        """
        try:
            # 创建文件夹
            tool.create_dir(base_dir)
            shelve_file = AccountDb.open()

            account_name = account.account_name
            del shelve_file[account_name]
            shelve_file.close()
            return True
        except ObjectError:
            return False


if __name__ == '__main__':
    # position = Position('00008', 100, 1.8)
    # account1 = Account('leo2', 18, 15, [position])
    # account1 = Account('leo3')
    # flag = AccountDb.save_account(account1)
    # rlt = AccountDb.delete_account(Account('leo2'))
    rlt_list = AccountDb.query_all()
    for rlt in rlt_list:
        print(rlt.account_name)
