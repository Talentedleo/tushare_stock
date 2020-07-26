from datetime import datetime

DATE_FORMATTER = '%Y%m%d'


# 结束日期为当天
def get_end_date():
    return datetime.now().strftime(DATE_FORMATTER)


if __name__ == '__main__':
    print(get_end_date())
