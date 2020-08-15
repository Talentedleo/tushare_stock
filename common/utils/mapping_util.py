def get_mapping_info(origin_df, mapping_df):
    name_list = []
    industry_list = []
    print('---- 正在匹配公司数据 ----')
    for _, row1 in origin_df.iterrows():
        for _, row2 in mapping_df.iterrows():
            if row1['ts_code'] == row2['ts_code']:
                name_list.append(row2['name'])
                industry_list.append(row2['industry'])
    origin_df['name'] = name_list
    origin_df['industry'] = industry_list

    return origin_df

