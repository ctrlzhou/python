# -*- coding: utf-8 -*-


# 代码学习自《Black Hat Python:Python Programming for Hackers and Pentesters》  
# 简易 UDP 客户端


import socket

target_host = "127.0.0.1"  # 本机回送地址（Loopback Address
target_port = 10000

# build a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
# send some data
for n in range(0,10):
    data = "test"
    print data
    client.sendto(data, (target_host, target_port))
# receive some data
   # data, addr = client.recvfrom(4096)  # 4k
    #if  not data :  # 如果接收服务器信息失败，或没有消息回应
     #   break
    print "打印的值%s" % data
client.close()