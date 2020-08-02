import os

import pandas as pd

# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + '/../../'
base_dir = os.path.abspath(project_path + '/storage')


def save_csv(df, file_name):
    file_path = base_dir + file_name
    df.to_csv(file_path)


def read_from_csv(file_name):
    file_path = base_dir + file_name
    return pd.read_csv(file_path)


def get_csv_name(pre, code, start_date, end_date):
    return '/' + pre + '/' + code.replace('.', '') + '_' + start_date + '_' + end_date + '.csv'


def get_csv_data_name(pre, code, end_date):
    return '/' + pre + '/' + code.replace('.', '') + '_' + end_date + '.csv'


def check_file_existed(file_name):
    return os.path.exists(base_dir + file_name)


if __name__ == '__main__':
    print(base_dir)
