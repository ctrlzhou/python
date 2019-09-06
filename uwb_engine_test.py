# -*- coding: UTF-8 -*-

import socket,time,threading

tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket---%s' % tcpClientSocket)

# serverAddr = ('192.168.10.93',5000)
serverAddr = ('192.168.10.171',52000)

tcpClientSocket.connect(serverAddr)
print('connect success!')

def get_tagid(num):
    tag_list = []
    for tag in range(0,num):
        tagid = hex(tag)[2:]   #去掉16进制的0x
        if len(tagid) == 1:    #不足两位的补0
            tagid = '0' + str(tagid)
        tag_list.append(tagid)
    print tag_list
    return(tag_list)

def uwb_data(tag_num,times):
    tag_list = get_tagid(tag_num)
    threads = []
    for tagid in tag_list:
        t = threading.Thread(target=single_data, args=(tagid, times,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

def single_data(tagid,times):
    num = 0
    while num < times:
        if num % 2 == 0:
            data =  "dc d90b 0000096b 000008c9 00000000 00000fa1 00000000 00000000 00000000 00000000 00000b49 00000000 00000000 0000148e 00000de8 00000000 00001717 0000172a 1072 63 007ee24d a%s:15" % tagid
        else:
            data =  "dc d90b 00000bb2 00000ca8 00000000 00000917 00000000 00000000 00000000 00000000 00000a73 00000000 00000000 00001261 00000a9c 00000000 00000faf 000013fa 147d ea 0080bcea a%s:15" % tagid
        tcpClientSocket.send(data)
        print data
        num += 1
        time.sleep(1)


print uwb_data(64,100000)
