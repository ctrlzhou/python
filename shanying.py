
#-*-coding:utf-8 -*-

from binascii import unhexlify
from twisted.internet import protocol, reactor
import time, string, crcmod, random

HOST = 'localhost'
PORT = 9000




class TSClntProtocol(protocol.Protocol):

    def loop_send(self,num,src_addr):
        flow_num = random.randint(1, 65535)
        for i in range(1,num):
            if flow_num > 65535:
                flow_num = 0
            flow_num = flow_num + 1
            flow_number = self.Hex_Inversion(flow_num)
            send_datas = self.send_datas(flow_number,src_addr)
            print "MAC地址为%s,第%s次发送：%s" %(src_addr,i,send_datas )
            send_data = self.strtoAscii(send_datas)
            self.sendData(send_data)
            time.sleep(30)

    def send_datas(self,flow_number,src_addr):

        data_dict = {}
        data_dict['startup'] = '7e'
        data_dict['flow_number'] = flow_number
        data_dict['protocol_number'] = '0102'
        data_dict['time_tags'] = self.timedataProcess()
        data_dict['source_address'] = src_addr
        data_dict['des_address'] = 'ffffffffffff'
        data_dict['app_datalength'] = ''
        data_dict['command_byte'] = '02'
        data_dict['app_data'] = '80010101'
        data_dict['checksum'] = ''
        data_dict['Terminator'] = '7e'
        data_dict['app_datalength'] = self.Hex_Inversion(len(data_dict['app_data'])/2)

        crcdata = data_dict['flow_number'] + data_dict['protocol_number'] + data_dict['time_tags'] + data_dict['source_address'] + data_dict['des_address'] \
                  + data_dict['app_datalength'] + data_dict['command_byte'] + data_dict['app_data']
        checksum = self.crc16Add(crcdata)
        send_datas = data_dict['startup'] + checksum + data_dict['Terminator']

        return (send_datas)

    def Hex_Inversion(self, num):

        hex_num = hex(num)[2:].zfill(4)
        #print hex_num
        hex_num = hex_num[2:] + hex_num[:2]  # 低位在前
        return (hex_num)

    def strtoAscii(self, str):

        data_list = []
        for k in range(1, len(str) + 1):
            if k % 2 == 0:
                data_list.append(str[(k-2):k])
        return_ascii = []
        #print data_list
        for i in data_list:
            return_ascii.append(chr(int(i, 16)))

        ascii = ''.join(return_ascii)  # list转str
        return (ascii)

    def timedataProcess(self):
        timedata = time.localtime(time.time())
        # print timedata
        year = timedata.tm_year
        year = str((str(year)[2:4])).zfill(2)
        year = str(hex(int(year))[2:])
        mon = str(hex(timedata.tm_mon)[2:]).zfill(2)
        day = str(hex(timedata.tm_mday)[2:]).zfill(2)
        hour = str(hex(timedata.tm_hour)[2:]).zfill(2)
        min = str(hex(timedata.tm_min)[2:]).zfill(2)
        sec = str(hex(timedata.tm_sec)[2:]).zfill(2)  # 不足2位前面补0
        data = sec + min + hour + day + mon + year
        return (data)

    def sourceAddr(self, mac):
        addr_list = mac.replace(":", '')
        return (addr_list)

    def sendData(self, data):
        # data = raw_input( )
        if data:
            #print '...sending %s...' % data
            self.transport.write(data)
        else:
            print 'end111'
            self.transport.loseConnection()

    def connectionMade(self):
        src_addr = "20F41B8003ED"
        num = 10
        self.loop_send(num,src_addr)

    def dataReceived(self, data):

        recdata_list = self.dataReceivedProcess(data)
        print ''.join(recdata_list)
        #if recdata_list(26) ==81
        # self.crc16Add(420b0102280b0a0f0)
        print self.sourceAddr("11:02:3E:44:55:66")

    def dataReceivedProcess(self, data):

        recdata_list = []
        print type(data)
        for i in data:
            recdata = hex(ord(i))[2:].zfill(2)
            recdata_list.append(recdata)
        return (recdata_list)

    def crc16Add(self, read):

        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        #print read
        # data = read.replace( , )
        readcrcout = hex(crc16(unhexlify(read))).upper()
        str_list = list(readcrcout)
        if len(str_list) == 5:
            str_list.insert(2, '0')  # 位数不足补0
        crc_data = ''.join(str_list)
        read = read + crc_data[4:] + crc_data[2:4]
        #print('CRC16校验', crc_data[4:] + crc_data[2:4])
        #print('增加Modbus CRC16校验：', read)
        return (read)


class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    clientConnectionLost = clientConnectionFailed = lambda self, connector, reason: reactor.stop()


reactor.connectTCP(HOST, PORT, TSClntFactory())
reactor.run()
