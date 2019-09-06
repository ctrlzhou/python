# -*- coding:utf8 -*-
from math import sqrt
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_data(time,station):

    so2 = []
    no2 = []
    o3 = []
    co = []
    pm25 = []
    pm10 = []
    data = {}
    db = MySQLdb.connect("119.29.152.124", "root", "zhilu", "zl_env",charset="utf8")
    cursor = db.cursor()
    sql = "SELECT so2,no2,o3,co,pm25,pm10 from zl_env_atmosphere_station_hour_data_history where `timelevel` like '%s%%' and station ='%s' ORDER BY `timelevel` ASC" % (time,station)
    print sql

    try:
        # 执行sql语句
        count = cursor.execute(sql)
        print "总共生效有%s行。"% count
        # 获取所有记录列表
        if count == 0:
            return count
        results = cursor.fetchall()
        #print results
        for row in results:
            so2.append(row[0])
            no2.append(row[1])
            o3.append(row[2])
            co.append(row[3])
            pm25.append(row[4])
            pm10.append(row[5])
        data['so2'] = so2
        data['no2'] = no2
        data['o3'] = o3
        data['co'] = co
        data['pm25'] = pm25
        data['pm10'] = pm10
        data['count'] = count
        return data
    except:
        # Rollback in case there is any error
        db.rollback()
        print "查询数据库失败"
    db.close()

def multipl(a, b):
    # 乘积之和
    sumofab = 0.0
    for i in range(len(a)):
        temp = a[i] * b[i]
        sumofab += temp
    return sumofab


def corrcoef(x, y):

    n = len(x)
    # 求和
    sum1 = sum(x)
    sum2 = sum(y)
    # 求乘积之和
    sumofxy = multipl(x, y)
    # 求平方和
    sumofx2 = sum([pow(i, 2) for i in x])
    sumofy2 = sum([pow(j, 2) for j in y])
    num = sumofxy - (float(sum1) * float(sum2) / n)
    # 计算皮尔逊相关系数
    den = sqrt((sumofx2 - float(sum1 ** 2) / n) * (sumofy2 - float(sum2 ** 2) / n))
    r = num / den
    return r**2

def deviation(list1,list2):
    list1 = [float(item) for item in list1]
    list2 = [float(item) for item in list2]

    sum1 = sum(list2)
    print len(list2)
    avg = sum1/len(list2)
    sdsq = sum([(i - avg) ** 2 for i in list1])
    stdev = (sdsq / (len(list2) - 1)) ** .5
    return stdev



def data_com(time,station1,station2):

    data1 = get_data(time,station1)
    data2 = get_data(time,station2)

    if (data1 != 0 and data2 != 0) and (data1['count'] == data2['count']):
        data1_so2 = data1['so2']
        data1_no2 = data1['no2']
        data1_o3  = data1['o3']
        data1_co  = data1['co']
        data2_so2 = data2['so2']
        data2_no2 = data2['no2']
        data2_o3 = data2['o3']
        data2_co = data2['co']

        so2_R2 = corrcoef(data1_so2,data2_so2)
        plot = "SO2"
        plotting(plot,data1_so2,data2_so2)
        print "SO2的皮尔逊相关系数平方为:%f" % so2_R2
        so2_dev = deviation(data1_so2,data2_so2)
        print "SO2的偏差值为：%f" % so2_dev
        no2_R2 = corrcoef(data1_no2, data2_no2)
        plot = "NO2"
        plotting(plot, data1_no2, data2_no2)
        print "NO2的皮尔逊相关系数平方为:%f" % no2_R2
        o3_R2 = corrcoef(data1_o3, data2_o3)
        plot = "O3"
        plotting(plot, data1_o3, data2_o3)
        print "O3的皮尔逊相关系数平方为:%f" % o3_R2
        co_R2 = corrcoef(data1_co, data2_co)
        plot = "CO"
        plotting(plot, data1_co, data2_co)
        print "CO的皮尔逊相关系数平方为:%f" % co_R2
    else:
        print "查询站点数据为空或是站点数值不相同！"



def plotting(plot,data1,data2):
    #X轴，Y轴数据
    x = np.arange(0,24,1)
    print x
    y1 = data1
    y2 = data2
    plt.figure(figsize=(10,6),dpi=80) #创建绘图对象
    plt.plot(x,y1,linestyle="-",linewidth=2,color="blue")   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.plot(x,y2,linestyle="-",linewidth=2,color="red")   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("hour") #X轴标签
    plt.ylabel("data")  #Y轴标签
    plt.title(plot) #图标题
    plt.show()  #显示图
    #plt.savefig("line.jpg") #保存图


#print(corrcoef(x, y))
time = "2018-04-10"
station1 = "赛百诺测试站点1"
station2 = "南油"
data_com(time,station1,station2)