import logging
import os

import common.utils.tool as tool
from common.utils import date_util as date

# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../../'
base_dir = os.path.abspath(project_path + '/log')


class Logger:

    def __init__(self, name='root'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel('DEBUG')
        BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
        # 输出到控制台的handler
        chlr = logging.StreamHandler()
        chlr.setFormatter(formatter)
        # 也可以不设置，不设置就默认用logger的level
        chlr.setLevel('INFO')
        # 创建文件夹
        tool.create_dir(base_dir)
        # 输出到文件的handler
        fhlr = logging.FileHandler(base_dir + '/log_' + date.get_now_date() + '.log')
        fhlr.setFormatter(formatter)
        self.logger.addHandler(chlr)
        self.logger.addHandler(fhlr)


if __name__ == '__main__':
    log = Logger(__name__).logger
    log.info('hello')
