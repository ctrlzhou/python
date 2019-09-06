# -*- coding:utf8 -*-

'''
import os, logging,time
if os.path.exists("D:/uwblog"):
    print "uwblog文件夹已经存在"
else:
    os.mkdir("D:/uwblog")
    print "uwblog文件夹创建成功"
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='D:/uwblog/%suwb.log' % time.strftime("%Y%m%d%H%M%S", (time.localtime(time.time()))),
    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

logging.info("测试日志")
'''
#!/usr/bin/env python
# coding=utf-8

# from xlwt import *
# #需要xlwt库的支持
# #import xlwt
# file = Workbook(encoding = 'utf-8')
# #指定file以utf-8的格式打开
# table = file.add_sheet('aaa')
# #指定打开的文件名

# data = {\
#         "1":["张三",150,120,100],\
#         "2":["wang",90,99,95],\
#         "3":["wu",60,66,68]\
#         }
# #字典数据
#
# ldata = []
# num = [a for a in data]
# #for循环指定取出key值存入num中
# num.sort()
# #字典数据取出后无需，需要先排序
#
# for x in num:
# #for循环将data字典中的键和值分批的保存在ldata中
#     t = [int(x)]
#     for a in data[x]:
#         t.append(a)
#     ldata.append(t)
#
# for i,p in enumerate(ldata):
# #将数据写入文件,i是enumerate()函数返回的序号数
#     for j,q in enumerate(p):
#         print i,j,q
#         table.write(i,j,q)
# file.save('aaa')
 # -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation
#
# pause = False
#
#
# def simData():
#     t_max = 10.0
#     dt = 0.05
#     x = 0.0
#     t = 0.0
#     while t < t_max:
#         if not pause:
#             x = np.sin(np.pi * t)
#             t = t + dt
#         yield t, x
#
#
# def onClick(event):
#     global pause
#     pause ^= True
#
#
# def simPoints(simData):
#     t, x = simData[0], simData[1]
#     time_text.set_text(time_template % (t))
#     line.set_data(t, x)
#     return line, time_text
#
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line, = ax.plot([], [], 'bo', ms=10)  # I'm still not clear on this stucture...
# ax.set_ylim(-1, 1)
# ax.set_xlim(0, 10)
#
# time_template = 'Time = %.1f s'  # prints running simulation time
# time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# fig.canvas.mpl_connect('button_press_event', onClick)
# ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=10,
#                               repeat=True)
# plt.show()

#-*- coding: utf-8 -*-

# import numpy as np
# import matplotlib.pyplot as plt
# #X轴，Y轴数据
# x = [0,1,2,3,4,5,6]
# y = [0.3,0.4,2,5,3,4.5,4]
# plt.figure(figsize=(8,4)) #创建绘图对象
# plt.plot(x,y,"r--",linewidth=2)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
# plt.xlabel("Time(s)") #X轴标签
# plt.ylabel("Volt")  #Y轴标签
# plt.title("Line plot") #图标题
# plt.show()  #显示图
# plt.savefig("line.jpg") #保存图


def flow_number(num):
    hex_num = hex(num)[2:].zfill(4)
    print hex_num
    hex_num = hex_num[2:]+hex_num[:2] # 低位在前
    print (hex_num)

#flow_number(255)

def dev_addr():
    Channel_number = "0"
    with open('Channel_number.txt', 'w') as single_Channel_number:
        for i in range(5, 11):
            Controller_number = str(i)
            for k in range(1, 11):
                Loop_number = str(k)
                for j in range(1, 256):
                    Address_number = str(j)
                    dev_addr = Controller_number + "-" + Loop_number + "-" + Address_number + "-" + Channel_number
                    print dev_addr
                    single_Channel_number.write(dev_addr + '\n')
dev_addr()