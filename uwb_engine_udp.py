# -*- coding: UTF-8 -*-

import time,threading,random
from socket import *

# serverAddr = ('192.168.10.93',5000)

udpCliSock = socket(AF_INET, SOCK_DGRAM)

def get_tagid(num):
    tag_list = []
    for tag in range(0,num):
        tagid = hex(tag)[2:]   #去掉16进制的0x
        if len(tagid) == 1:    #不足两位的补0
            tagid = '0' + str(tagid)
        tag_list.append(tagid)
    print tag_list
    return(tag_list)

def convert_hex(num):
    hex_num = hex(num)[2:]   #去掉16进制的0x
    if len(hex_num) == 1:    #不足两位的补0
        hex_num = '0' + str(hex_num)
    return(hex_num)

def uwb_data(ADDR,tag_num,times,anchor_falg):
    tag_list = get_tagid(tag_num)
    threads = []
    for tagid in tag_list:
        t = threading.Thread(target=single_data, args=(ADDR,tagid, times,anchor_falg,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

def single_data(ADDR,tagid,times,anchor_falg):
    num = 0
    sn = 0
    data_list = []
    if anchor_falg ==1:
        a = "dc 001f 00001a61 000012c7 00000d6b 000016bc 000029cc 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "
        b = "dc 003f 00001887 000013b5 00000d27 000015b1 00002c3b 00003225 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "
        c = "dc 0001 00001f9c 00001288 00000f2c 00001b5f 00002a5d 000035d2 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "
    if anchor_falg ==2:
        a = "dc 00000001 00001a61 000012c7 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "\
            "00000000 00000000 00000000 00000d6b 00000000 00000000 000016bc 00000000 000029cc 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "
        b ="dc 00000001 00001887 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00002c3b 00000000 00000000 00003225 00000000 00000000 00000000 "\
            "00000000 00000000 00000000 00000000 000013b5 00000000 00000000 00000000 00000000 00000000 00000000 00000000 000015b1 00000000 00000000 00000d27 "
        c ="dc 00000001 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 "\
            "00000000 00001f9c 00000000 00000000 00001288 00000000 00000f2c 00000000 00001b5f 00000000 00002a5d 00000000 00000000 00000000 00000000 000035d2 "
    data_list.append(a)
    data_list.append(b)
    data_list.append(c)
    print data_list

    while num < times:
        num_hex = convert_hex(sn)
        fix_data = data_list[random.randint(0,len(data_list)-1)]
        print "标签号为%s,发送的坐标" % tagid
        for i in range(0,6):
            anchor = '0' + str(i)
            data = fix_data + "2c87 %s 003ee231 a%s:%s ff 5f 02" % (num_hex,tagid,anchor)
            udpCliSock.sendto(data, ADDR)
            print data
        #data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        num += 1
        sn +=1
        if sn > 255:
            sn = 0
        time.sleep(0.2)

#udpCliSock.close()

ADDR = ('192.168.10.171',52000)
#BUFSIZE = 1024s
tagid_num = 1
times =1000000
anchor_falg = 1 #1代表16个基站，2代表是32个基站
print uwb_data(ADDR,tagid_num,times,anchor_falg)
