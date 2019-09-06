# -*-coding:utf-8 -*-
import socket
import random, threading,time


def tcp_Client(host, port):
    HOST = host
    PORT = port
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        time.sleep(1)
        data = send_Tcpdata(2222123)
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        print(data)
    tcpCliSock.close()

def udp_Client(host,port):
    HOST = host
    PORT = port
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    udpCliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpCliSock.connect(ADDR)
    while True:
        time.sleep(1)
        data = send_Udpdata(71069)
        if not data:
            break
        udpCliSock.sendto(data, ADDR)
        data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        if not data:
            break
        print(data)
    udpCliSock.close()

def send_Udpdata(number):
    # 03, 867726037131655, 89860424121880850166, NBSMOKE, NORMAL, 320, 940, -125, 10, -DSOC / 096, -SM / 029,
    # 04, 867726037131655, 89860424121880850166, NBSMOKE, KEYTEST,
    # 05, 867726037131762, 898607b7061890523838, NBSMOKE, ALARM,
    Number = number
    SIM_num = "89860618000036669674"
    status_list = ["KEYTEST","BATFAULT","NORMAL"]
    status = random.choice(status_list)
    DSOC = str(random.randint(1,100)).zfill(3)
    SM   = str(random.randint(1,100)).zfill(3)
    data1 = "03, %s, %s, NBSMOKE, NORMAL, 320, 940, -125, 10, -DSOC / %s, -SM / %s," %(Number,SIM_num,DSOC,SM)
    data2 = "04, %s, %s, NBSMOKE, %s," %(Number,SIM_num,status)
    data3 = "05, %s, %s, NBSMOKE, ALARM," %(Number,SIM_num)
    data_list = [data1,data2,data3]
    data = random.choice(data_list)
    print data
    return data



def send_Tcpdata(number):
    Number = number
    SIM_num = "89860618000036669674"
    status_list = ["BATFAULT", "FAULT", "START", "NORMAL"]
    status = random.choice(status_list)
    num = random.randint(0, 100)
    if num > 50:
        device_status = 'ALARM'
    else:
        device_status = 'NORMAL'
    DSOC = str(num).zfill(3)
    data1 = "NBAVFAPP:%s,%s,%s,-DSOC / %s" % (Number, SIM_num, device_status, DSOC)
    data2 = "NBAVFAPP:%s,%s,%s" % (Number, SIM_num, status)
    data_list = [data1, data2]
    data = random.choice(data_list)
    print data
    return data


def thread_send(tag_id, count):
    threads = []
    for tag in tag_id:
        t = threading.Thread(target=tcp_Client, args=(tag, count,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    #tcp那个只有9002  udp的是9003
    host = "123.207.39.248"
    udp_port = 9003
    tcp_port = 9002
    udp_Client(host, udp_port)
