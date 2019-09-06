import socket
from time import ctime

def udp_Server():

    HOST = ''
    PORT = 8099
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSerSock.bind(ADDR)
    while True:
        print("等待连接......")
        data, addr = udpSerSock.recvfrom(BUFSIZE)
        udpSerSock.sendto('[%s] %s' % (ctime(), data), addr)
        print("...接收到连接：", addr)
    udpSerSock.close()


def udp_Client():
    HOST = 'localhost'
    PORT = 8099
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    udpCliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpCliSock.connect(ADDR)
    while True:
        data = input("> ")
        if not data:
            break
        udpCliSock.sendto(data, ADDR)
        data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        if not data:
            break
        print(data)
    udpCliSock.close()

def tcp_Client():

    HOST = 'localhost'
    PORT = 8099
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        data = input("> ")
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        print(data)
    tcpCliSock.close()

def tcp_Server():
    HOST = ''
    PORT = 8099
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    while True:
        print("等待连接......")
        tcpCliSock, addr = tcpSerSock.accept()
        print("...接收到连接：", addr)
        while True:
            data = tcpSerSock.recv(BUFSIZE)
            if not data:
                break
            tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        tcpCliSock.close()
    tcpSerSock.close()