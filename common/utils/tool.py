import os


def create_dir(path):
    folder = os.path.exists(path)
    # 判断是否存在文件夹如果不存在则创建为文件夹
    if not folder:
        # 创建文件时如果路径不存在会创建这个路径
        os.makedirs(path)
