# -*- coding: utf-8 -*-

"""
    作者：     小汪仙人
    版本：     1.0
    日期：     2019.5.14
    文件名：   main.py

    数据分析及可视化案例
    任务：
         - 绘制出一线城市历史房价图

    数据来源：https://www.anjuke.com/fangjia/
"""

import pandas as pd
from matplotlib import pyplot as plt
from pyecharts import Bar, Line

import config

def create_look_year_data(data_df , city, year):
    """
        使用matplotlib绘制
            绘制出城市的某年房价折线图
    """
    data_copy = data_df[(data_df['city'] == city) & (data_df['year'] == year)]
    data_copy = data_copy.sort_values('month')
    data_copy = data_copy.set_index('month')
    plt.plot(data_copy['price'], 'o-')
    plt.show()

def create_look_data(data_df, city):
    """
        分组求均值操作
            按年求均值
            返回处理后数据
    """
    data_copy = data_df[(data_df['city'] == city)]
    data_copy = data_copy.groupby(['year', 'city']).mean().round()
    data_copy.reset_index(inplace=True)

    return data_copy

def create_look_city_line(data_df, city):
    """
        绘制出城市每个区的历史房价折线图
    """
    data_copy = data_df[(data_df['city'] != city)]
    data_index = data_copy.groupby('city').mean().round()
    data_index.reset_index(inplace=True)
    data_copy = data_copy.groupby(['year', 'city']).mean().round()
    data_copy.reset_index(inplace=True)
    line = Line(city+'各区历史房价', '2010-2019'+city+'各区历史房价折线图')
    for i in data_index['city']:
        line.add(i, data_copy[data_copy['city'] == i]['year'], data_copy[data_copy['city'] == i]['price'],
                 is_label_show=True, legend_top='bottom')
    line.render(config.out_path + city + '.html')

def main():

    # 分别取出数据
    data_df = {i: pd.read_csv(config.data_path+i+'.csv', usecols=config.usecols) for i in config.data_names}

    # 实例化Bar
    bar = Bar('一线城市历史房价', '2010-2019一线城市房价柱状图')

    # 循环绘制出三个城市的历史房价
    for k, v in data_df.items():
        date = create_look_data(v, k)
        create_look_city_line(v, k)
        bar.add(k, date['year'], date['price'], mark_line=['average'])

    # 保存结果
    bar.render(config.out_path+'fangjia.html')

__name__ == '__main__' and main()