# -*- coding: UTF-8 -*-
import socket, time, re, math, json

tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket---%s' % tcpClientSocket)

# serverAddr = ('192.168.10.93',5000)
serverAddr = ('192.168.10.171',52000)

tcpClientSocket.connect(serverAddr)
print('connect success!')


def uwbdata_datatype1():
    x = 1
    jizhan1 = 00000000
    while x < 20:
        n = str(hex(jizhan1))
        s = n.zfill(8)
        # assert s == "00123"
        # print s
        s1 = re.sub('[x]', '', s)
        # print s1
        s2 = s1.zfill(8)
        # print s2
        jizhan1 = jizhan1 + 1
        x = x + 1
        uwbdata = 'mc 0f 0000031d 000002b1 00000000 ' + str(s2) + ' 0a67 58 0000e690 a2:3'
        tcpClientSocket.send(uwbdata)
        time.sleep(0.1)
        print uwbdata


def uwbdata_datatype2():
    A0 = 2
    x = y = z = w = 2000
    while A0 < 2828:
        # x=1
        # jizhan2=00000000
        A1 = math.sqrt(pow((x - math.sqrt(A0 / 2)), 2) + pow(math.sqrt(A0 / 2), 2))
        A2 = math.sqrt(pow((x - math.sqrt(A0 / 2)), 2) + pow(math.sqrt(A0 / 2), 2))
        A3 = math.sqrt(2 * (pow(x, 2))) - A0
        # print int(A0),int(A1),int(A2),int(A3)

        sA0 = str(hex(int(A0))).zfill(8)
        sA01 = re.sub('[x]', '', sA0)
        sA02 = sA01.zfill(8)

        sA1 = str(hex(int(A1))).zfill(8)
        sA11 = re.sub('[x]', '', sA1)
        sA12 = sA11.zfill(8)

        sA2 = str(hex(int(A2))).zfill(8)
        sA21 = re.sub('[x]', '', sA2)
        sA22 = sA21.zfill(8)

        sA3 = str(hex(int(A3))).zfill(8)
        sA31 = re.sub('[x]', '', sA3)
        sA32 = sA31.zfill(8)

        # print 'mc 0f ' +str(sA02)+ ' ' +str(sA12)+ ' ' +str(sA22)+ ' ' +str(sA32)+' 0a67 58 0000e690 a2:3'
        # while x<20:
        # n = str(hex(jizhan2))
        # s = n.zfill(8)
        # assert s == "00123"
        # print s
        # s1 = re.sub('[x]', '', s)
        # print s1
        # s2 = s1.zfill(8)
        # print s2
        # jizhan2=jizhan2+1
        # x=x+1
        uwbdata = 'mc 0f ' + str(sA02) + ' ' + str(sA12) + ' ' + str(sA22) + ' ' + str(sA32) + ' 0a67 58 0000e690 a1:0'
        tcpClientSocket.send(uwbdata)
        time.sleep(0.1)
        A0 = A0 + 1
        print uwbdata


def uwbdata_datatype3():
    x = 1
    jizhan3 = 00000000
    while x < 20:
        n = str(hex(jizhan3))
        s = n.zfill(8)
        # assert s == "00123"
        # print s
        s1 = re.sub('[x]', '', s)
        # print s1
        s2 = s1.zfill(8)
        # print s2
        jizhan3 = jizhan3 + 1
        x = x + 1
        uwbdata = 'mc 0f 0000031d ' + str(s2) + ' 000002b1 000002b1 0a67 58 0000e690 a2:3'
        tcpClientSocket.send(uwbdata)
        time.sleep(0.1)
        print uwbdata


def uwbdata_datatype4():
    x = 1
    jizhan4 = 00000000
    while x < 20:
        n = str(hex(jizhan4))
        s = n.zfill(8)
        # assert s == "00123"
        # print s
        s1 = re.sub('[x]', '', s)
        # print s1
        s2 = s1.zfill(8)
        # print s2
        jizhan4 = jizhan4 + 1
        x = x + 1
        uwbdata = 'mc 0f ' + str(s2) + ' 0000031d 000002b1 000002b1 0a67 58 0000e690 a2:3'
        tcpClientSocket.send(uwbdata)
        time.sleep(0.1)
        print uwbdata
        # datatype:


        # uwbdata_datatype1()
        # uwbdata_datatype2()
        # uwbdata_datatype3()
        # uwbdata_datatype4()
        # while True:

        # sendData = raw_input('please input the send message:')
        # sendData = 'mc 03 0000031d 000002b1 00000000 00000000 0a67 58 0000e690 a2:3'
        # nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(nowtime + ' sendData is:%s' %sendData)
        # sendData=uwbdata(0)

        # if len(sendData)>0:
        #   tcpClientSocket.send(sendData)
        #  time.sleep(1)
        # else:
        #   break


        # recvData = tcpClientSocket.recv(1024)

        # print('the receive message is:%s'%recvData)





def uwbdata():
    x = 1
    while x < 20000:
        uwbdata1 = 'ma 0e 00000000 000011bf 00000dfe 000015fd dec5 f8 04bd5413 a0:0'
        tcpClientSocket.send(uwbdata1)
        print uwbdata1
        time.sleep(1)

        uwbdata2 = 'mc 07 00000f38 00000cdb 00000e52 00000000 e006 c3 04bd6617 a0:0'
        tcpClientSocket.send(uwbdata2)
        print uwbdata2
        time.sleep(1)

        uwbdata3 = 'mr 0f 00000ea3 00000c33 00000dbd 000000ce df31 a4 40224022 a0:0'
        tcpClientSocket.send(uwbdata3)
        print uwbdata3
        time.sleep(1)

        uwbdata4 = 'ma 0e 00000000 000011ba 00000e28 00001461 df9d 17 04bd602f a0:0'
        tcpClientSocket.send(uwbdata4)
        print uwbdata4
        time.sleep(1)

        uwbdata5 = 'mc 0f 00000f12 00000ce5 00000e60 000001a6 e28a 20 04bd8a6b a0:0'
        tcpClientSocket.send(uwbdata5)
        print uwbdata5
        time.sleep(1)

        uwbdata6 = 'mr 07 00000eb6 00000c4f 00000dd0 00000000 e006 c3 40224022 a0:0'
        tcpClientSocket.send(uwbdata6)
        print uwbdata6
        time.sleep(1)

        x = x + 1


def uwbdatafromfile():
    while True:
        line_nu = 0
        # file = open("data12.txt")
        print time.time()
        file = open("302chuanjian.txt")
        for line in file:
            if line_nu < 13742:
                if line_nu % 2 == 0:
                    # time.sleep(1)
                    print 'wait 1 second'
                    print(line.strip())
                tcpClientSocket.send(line.strip())
                line_nu += 1
                # if line_nu % 32 ==0:
                #   print 'wait 3 second'
                time.sleep(0.2)
            else:
                break
        file.close()
        # uwbdata()





uwbdatafromfile()

tcpClientSocket.close()
print('close socket!')
