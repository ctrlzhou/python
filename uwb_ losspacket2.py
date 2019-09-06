# -*- coding:utf8 -*-
import socket, traceback,time,threading,logging,os


class losspacket():
    if os.path.exists("D:/uwblog"):
        print "uwblog文件夹已经存在"
    else:
        os.mkdir("D:/uwblog")
        print "uwblog文件夹创建成功"
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    logging.basicConfig(
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        level=logging.DEBUG,
        filename='D:/uwblog/uwblosspacket%s.log' % time.strftime("%Y%m%d%H%M%S", (time.localtime(time.time()))),
        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)

    global loss_zero
    loss_zero = {} # 值为0值的个数


    def __init__(self,host,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

    def receive_data(self,anchor_list):
        global loss_zero
        time_list = []
        loss_num = 0  # 丢包个数
        count_num = 0  # 总的发包个数
        dir_anchordata = {}#定义一个接收基站的字典
        for anchor in anchor_list: #把基站为0的总个数初始化
            loss_zero[anchor] = 0
        while 1:
            try:
                message, address = self.s.recvfrom(8192)
                logging.info("Got data from%s,:%s" % (address,message))
                now_time = time.time()
                time_list.append(now_time)
                num = self.loss_time(time_list, count_num, loss_num)
                count_num = num[0]
                loss_num = num[1]
                # 返回所有基站的数据
                for anchor in anchor_list:
                    dir_anchordata[anchor] = self.get_GroupData(message, anchor)
                self.thread_GetNum(dir_anchordata, count_num, loss_num)
                self.s.sendto("abc", address)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()

    def get_GroupData(self,str,anchor):
        groupdata = {}
        tmp_str = str.split(" ")
        num = len(str)/176 # 176是一个基站发送的长度
        for i in range(0,num):
            if i == 0:
                j = anchor + 2
            elif i == 1:
                j = anchor + 23
            elif i == 2:
                j = anchor + 44
            elif i == 3:
                j = anchor + 65
            n = i*21
            anchor_num = self.get_Anchor(str,n)
            groupdata[anchor_num] = tmp_str[j]
        return groupdata


    def get_AnchorData(self,str, num):
        num = num + 2
        return str.split(" ")[num]

    def get_Tag(self,str):
        tmp_str = self.get_AnchorData(str, 19)
        return tmp_str.split(":")[0]


    def get_Anchor(self,str,num):
        num = num + 19
        tmp_str = self.get_AnchorData(str, num)
        return_str = tmp_str.split(":")[1].split() # 后面那个split是去掉/r/n
        return int(return_str[0], 16) #将16进制转换成10进制



    def thread_GetNum(self,dir_anchordata, count_num, loss_num):
        # 多进程进行正常坐标和告警坐标

        threads = []
        anchor = 1
        logging.info(dir_anchordata)
        for (k,v) in dir_anchordata.items():
            t = threading.Thread(target=self.get_LossNum, args=(k,v, count_num, loss_num))
            threads.append(t)
            anchor += 1

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()


    def loss_time(self,time_list, count_num, loss_num):
        if len(time_list) >= 2:
            timelevel = time_list[-1] - time_list[-2]
            if 1 < timelevel < 1.4:  # 定时上报时间是1.32秒
                count_num += 1
            else:
                count = int(timelevel / 1.32)
                print count
                count_num += count
                loss_num += (count - 1)
        else:
            count_num += 1
        num = [count_num, loss_num]
        return num

    def get_LossNum(self, anchor,dir_data, count_num, loss_num):
        global loss_zero
        flag = 0
        for (k,v) in dir_data.items():
            if v != "00000000":
                flag = 0
                break
            else:
                flag = 1
        if flag == 1:
            loss_zero[anchor] += 1
        logging.info("%d号基站，总发包数是%d,丢包个数是%d,为0的值个数是%d" % (anchor, count_num, loss_num, loss_zero[anchor]))
        if count_num == 100 or count_num % 500 == 0:
            self.loss_Percent(anchor, count_num, loss_num, loss_zero[anchor])


    def loss_Percent(self,anchor, count_num, loss_num, loss_zero):
        percent = (float(loss_num + loss_zero) / count_num) * 100
        logging.info("%d号基站，%d个包的丢包率是：%s个百分点，丢包个数是：%d,值为0的个数：%d" % (anchor,count_num, percent, loss_num, loss_zero))

if __name__ == '__main__':
    host = "192.168.10.87"
    port = 5006
    anchor_list = [0, 1, 14, 15]
    p = losspacket(host,port)
    p.receive_data(anchor_list)

