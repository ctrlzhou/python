# -*- coding:utf8 -*-
import socket, traceback,time,threading



class losspacket():
    global loss_zero  # 值为0值的个数
    loss_zero = {}


    def __init__(self,host,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

    def receive_data(self,anchor_list):
        global loss_zero
        data_list = []
        loss_num = 0  # 丢包个数
        count_num = 0  # 总的发包个数

        for anchor in anchor_list: #把基站为0的总个数初始化
            loss_zero[anchor] = 0
        while 1:
            try:
                message, address = self.s.recvfrom(8192)
                print "Got data from", address, ": ", message
                now_time = time.time()
                groupdata = self.get_GroupData(message,now_time)
                data_list.append(groupdata)
                self.loss_time(message,data_list, count_num, loss_num)
                self.s.sendto("abc", address)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()


    def get_AnchorData(self,str, num):
        num = num + 2
        return str.split(" ")[num]


    def get_Tag(self,str):
        #获取标签的ID号
        tmp_str = self.get_AnchorData(str, 19)
        return tmp_str.split(":")[0]

    def get_SerialNum(self,str):
        #获取数据中的序列号
        serialnum = self.get_AnchorData(str, 17)
        return int(serialnum, 16)

    def get_Anchor(self,str):
        #获取基站的编号
        tmp_str = self.get_AnchorData(str, 19)
        return tmp_str.split(":")[1]

    def get_GroupData(self,str,time):
        serialnum = self.get_SerialNum(str)
        anchoraddress = self.get_Anchor(str)
        groupdata = [time,serialnum,anchoraddress]
        return groupdata

    def thread_GetNum(self,dir_anchordata, count_num, loss_num):
        # 多进程进行正常坐标和告警坐标

        threads = []
        anchor = 1
        for (k,v) in dir_anchordata.items():
            t = threading.Thread(target=self.get_LossNum, args=(k,v, count_num, loss_num))
            threads.append(t)
            anchor += 1

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()


    def loss_time(self,message,data_list, count_num, loss_num):
        dir_anchordata = {}  # 定义一个接收基站的字典
        print data_list

        if len(data_list) >= 2:
            serialnum = data_list[-2][1]
            if data_list[-1] == serialnum:
                Anchor = data_list[-1][2]
                for anchor in anchor_list:
                    dir_anchordata[Anchor][anchor] = self.get_AnchorData(message, anchor)
                print "aaaaaaaaa%d" % dir_anchordata
            timelevel = data_list[-1][0] - data_list[-2][0]
            if 1 < timelevel < 1.4:  # 定时上报时间是1.32秒
                count_num += 1
            else:
                count = int(timelevel / 1.32)
                print count
                count_num += count
                loss_num += (count - 1)
        else:
            count_num += 1

        print "发包总数:%d,丢包数:%d" % (count_num, loss_num)
        for anchor in anchor_list:
            dir_anchordata[anchor] = self.get_AnchorData(message, anchor)
        self.thread_GetNum(dir_anchordata, count_num, loss_num)


    def get_LossNum(self, anchor,data, count_num, loss_num):
        global loss_zero
        if data == "00000000":
                loss_zero[anchor] += 1
        print "%d号基站，总发包数是%d,丢包个数是%d,为0的值个数是%d" % (anchor, count_num, loss_num, loss_zero[anchor])
        if count_num == 100 or count_num%500 == 0:
            self.loss_Percent(anchor, count_num, loss_num, loss_zero[anchor])


    def loss_Percent(self,anchor, count_num, loss_num, loss_zero):
        percent = (float(loss_num + loss_zero) / count_num) * 100
        print "%d号基站，%d个包的丢包率是：%s个百分点，丢包个数是：%d,值为0的个数：%d" % (anchor,count_num, percent, loss_num, loss_zero)

if __name__ == '__main__':
    host = "192.168.10.87"
    port = 6666
    anchor_list = [0, 1, 14, 15]
    p = losspacket(host,port)
    p.receive_data(anchor_list)

