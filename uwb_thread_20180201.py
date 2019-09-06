# -*- coding:utf8 -*-
import socket, time, random, json, os
import threading
import logging


class uwb():
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
        filename='D:/uwblog/%suwb.log' % time.strftime("%Y%m%d%H%M%S", (time.localtime(time.time()))),
        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        logging.debug('Strange error creating socket:%s' % e)
    server_address = ""  # 服务器地址
    tag_list = []  # tag列表
    G_pos_code = {}  # 告警信息中的pos_code
    alarm_len = 0  # 告警列表中的长度

    def __init__(self, ip, port, sleep):
        self.server_address = (ip, port)
        logging.info('Connecting to %s:%s.' % self.server_address)
        self.sock.connect(self.server_address)
        self.sleep = sleep

    def send_data(self, room, tag, count):
        # 发送数据函数
        try:
            if len(tag) != 0:
                if len(tag) == 1:
                    tag_id = tag[0]
                    self.single_num(count, tag_id)
                else:
                    tag_id = tag
                    self.mul_num(count, tag_id)
            else:
                tag_id = self.select_room(room)
                self.mul_num(count, tag_id)
        except socket.error, arg:
            logging.debug('获取异常 %s' % arg)

    def send_alarm_data(self, tag, alarm_type):
        # 发送单个TAG的告警数据函数
        if tag not in self.tag_list:
            pose_code = self.get_pos_code(tag)
            data = self.alarm_data(tag, pose_code, 4, 0)  # 先发发送一个取消信号消失的告警
            logging.info("取消信号消失%s" % data)
            self.sock.sendall(data + "*")
            self.tag_list.append(tag)
        send_data = []
        for num in range(0, 10):
            if num == 0:
                data = self.normal_data(tag)
                logging.info(data)
                send_data.append(data)
            else:
                data = self.second_data(tag, data)
                logging.info(data)
                send_data.append(data)
        for data in send_data:
            self.sock.sendall(data + "*")
            time.sleep(self.sleep)
        self.start_alarm(tag, alarm_type, data)
        last_data = self.cancel_alarm(tag, alarm_type)
        self.G_pos_code[tag] = self.return_pos_code(last_data)

    def single_num(self, count, tag):
        # 单个tag发送数据函数
        if tag not in self.tag_list:
            pose_code = self.get_pos_code(tag)
            data = self.alarm_data(tag, pose_code, 4, 0)  # 先发发送一个取消信号消失的告警
            logging.info("取消信号消失%s" % data)
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常1 %s" % arg)
                logging.info('again Connecting to %s:%s.' % self.server_address)
                self.sock.connect(self.server_address)
            self.tag_list.append(tag)
            # print tag_list
            logging.info("发送报警坐标")
            self.alarm_flow(tag, count)

    time.sleep(10)

    def get_pos_code(self, tag):
        if tag < 12:
            pos_code = "0101030900"

        elif tag < 24:
            pos_code = "0101031000"

        elif tag < 36:
            pos_code = "0101031100"

        elif tag < 48:
            pos_code = "0101041000"

        elif tag < 60:
            pos_code = "0101021200"

        return pos_code

    def mul_num(self, count, tag_id):
        # 发送多个tag数据函数
        for tag in tag_id:
            pose_code = self.get_pos_code(tag)
            data = self.alarm_data(tag, pose_code, 4, 0)  # 先发发送一个取消信号消失的告警
            logging.info("取消信号消失%s" % data)
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常1 %s" % arg)
                logging.info('again Connecting to %s:%s.' % self.server_address)
                self.sock.connect(self.server_address)
            self.tag_list.append(tag)

        self.thread_send(tag_id, count)

    def interval_senddata(self, tag, count):
        # 循环间隔发送数据
        if self.alarm_len == 0:
            num = 50
        else:
            num = self.alarm_len
        COUNT = num * count
        logging.info("当前正常的值%s" % COUNT)
        for num in range(0, COUNT):
            if num == 0:
                data = self.normal_data(tag)
                self.sock.sendall(data + "*")
            else:
                data = self.second_data(tag, data)
                self.sock.sendall(data + "*")
            time.sleep(self.sleep)
            logging.info("正常坐标%s" % data)
        self.G_pos_code[tag] = self.return_pos_code(data)

    def second_data(self, tag, first_data):
        # 第一个正常坐标数据后发送的坐标
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        data['pos_code'] = self.return_pos_code(first_data)
        pos_x = float(self.return_pos_x(first_data))
        pos_y = float(self.return_pos_y(first_data))

        if data['pos_code'] == "0101030900":
            data['pos_x'] = self.get_coordinate(2.675, 0.105, pos_x)

        elif data['pos_code'] == "0101031000":
            data['pos_x'] = self.get_coordinate(5.35, 2.78, pos_x)

        elif data['pos_code'] == "0101031100":
            data['pos_x'] = self.get_coordinate(8.025, 5.455, pos_x)

        elif data['pos_code'] == "0101041000":
            data['pos_x'] = self.get_coordinate(5.35, 2.78, pos_x)

        elif data['pos_code'] == "0101021200":
            data['pos_x'] = self.get_coordinate(10.805, 8.13, pos_x)

        else:
            data['pos_x'] = round(random.uniform(1, 5), 4)

        if pos_y == 0.5:
            data['pos_y'] = 0.5
        else:
            data['pos_y'] = self.get_coordinate(4.385, 0.6, pos_y)

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return jsonData

    def get_coordinate(self, max, min, pos):
        # 返回当前坐标最大值和最小值中间的坐标
        if pos + 0.4 < max:
            if pos - 0.4 > min:
                pos1 = round(pos - random.uniform(0, 0.4), 4)
                pos2 = round(pos + random.uniform(0, 0.4), 4)
                pos3 = pos
                data_pos = random.choice([pos1, pos2, pos3])
            else:
                data_pos = round(pos + random.uniform(0, 0.4), 4)
        else:
            data_pos = round(pos - random.uniform(0, 0.4), 4)
        return data_pos

    def thread_send(self, tag_id, count):
        # 多进程进行正常坐标和告警坐标
        threads = []
        for tag in tag_id:
            if tag % 10 == 0:
                t = threading.Thread(target=self.alarm_flow, args=(tag, count,))
                threads.append(t)
            else:
                t = threading.Thread(target=self.interval_senddata, args=(tag, count,))
                threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()
            # self.sock.sendall(data+"*")
        time.sleep(2)
        print "多线程测试结束"

    def alarm_flow(self, tag, count):
        # 发送告警坐标，告警到取消告警的一个过程
        for i in range(0, count):
            send_data = []
            for num in range(0, 5):
                if num == 0:
                    data = self.normal_data(tag)
                    logging.info(data)
                    send_data.append(data)
                else:
                    data = self.second_data(tag, data)
                    logging.info(data)
                    send_data.append(data)
            for data in send_data:
                self.sock.sendall(data + "*")
                time.sleep(self.sleep)
            self.mul_alarm(tag, data)
            # self.single_alarm(tag,data)

    def single_alarm(self, tag, data):  # 单个告警
        # 单个告警
        alarm_type = random.randint(1, 4)
        self.start_alarm(tag, alarm_type, data)
        last_data = self.cancel_alarm(tag, alarm_type)
        self.G_pos_code[tag] = self.return_pos_code(last_data)  # 获取最后一个坐标的pos_code

    def mul_alarm(self, tag, data):  # 多个告警
        # 多个告警
        flag = random.randint(0, 4)
        if flag == 0:
            self.single_alarm(tag, data)
        elif flag == 1:  # 先串仓再信号消失
            data_one = self.start_alarm(tag, 1, data)
            self.start_alarm(tag, 4, data_one)
            time.sleep(5)
            self.cancel_alarm(tag, 1)
            last_data = self.cancel_alarm(tag, 4)
            self.G_pos_code[tag] = self.return_pos_code(last_data)
        elif flag == 2:  # 先串仓再电子围栏
            data_one = self.start_alarm(tag, 1, data)
            self.start_alarm(tag, 2, data_one)
            time.sleep(5)
            self.cancel_alarm(tag, 1)
            last_data = self.cancel_alarm(tag, 2)
            self.G_pos_code[tag] = self.return_pos_code(last_data)
        elif flag == 3:  # 先厕所滞留，再电子围栏
            data_one = self.start_alarm(tag, 3, data)
            self.start_alarm(tag, 2, data_one)
            time.sleep(5)
            self.cancel_alarm(tag, 2)
            last_data = self.cancel_alarm(tag, 3)
            self.G_pos_code[tag] = self.return_pos_code(last_data)
        elif flag == 4:  # 先厕所滞留，再串仓
            data_one = self.start_alarm(tag, 3, data)
            self.start_alarm(tag, 1, data_one)
            self.cancel_alarm(tag, 1)
            last_data = self.cancel_alarm(tag, 3)
            self.G_pos_code[tag] = self.return_pos_code(last_data)

    def return_pos_code(self, data):
        return data[19:29]
        # return data.split()[2]

    def return_pos_x(self, data):
        x = data.split()[4]
        return x.split(",")[0]

    def return_pos_y(self, data):
        y = data.split()[6]
        return y.split(",")[0]

    def start_alarm(self, tag, alarm_type, data):
        # 发送告警
        send_data = []  # 把发送的坐标放入到列表中
        if alarm_type == 2 or alarm_type == 4:
            pos_code = self.return_pos_code(data)  # 获取最后一次正常坐标的pos_code
        data = self.invalid_data(tag, alarm_type)  # 发送告警坐标
        send_data.append(data)
        alarm_data = data
        # room = self.return_room(data)
        if alarm_type == 1 or alarm_type == 3:
            pos_code = self.return_pos_code(data)  # 获取当前告警坐标的监狱pos_code
        data = self.alarm_data(tag, pos_code, alarm_type, 1)  # 发送告警
        logging.info("gaojing %s" % data)
        send_data.append(data)

        for num in range(0, 15):  # 再连续发送15次告警坐标
            if alarm_type == 4:
                last_data = 'sleep1'
            else:
                last_data = self.second_data(tag, alarm_data)
            send_data.append(last_data)

        self.alarm_len = len(send_data)

        for data in send_data:
            if data == 'sleep1':
                time.sleep(self.sleep)
                continue
            else:
                self.sock.sendall(data + "*")
                logging.info("报警的坐标%s" % data)
                time.sleep(self.sleep)
        return data  # 返回最后一次的坐标

    def cancel_alarm(self, tag, alarm_type):
        # 结束告警
        # type: (object, object) -> object
        send_data = []
        pos_code = self.get_pos_code(tag)
        data = self.alarm_data(tag, pos_code, alarm_type, 0)  # 取消告警
        logging.info("quxiaogaojing %s" % data)
        send_data.append(data)
        for num in range(0, 5):
            if num == 0:
                data = self.normal_data(tag)  # 再发送正常坐标
                send_data.append(data)
            else:
                data = self.second_data(tag, data)
                send_data.append(data)
        self.alarm_len += len(send_data)
        print "显示的长度%s" % self.alarm_len
        for data in send_data:
            if data == 'sleep1':
                time.sleep(self.sleep)
                continue
            else:
                try:
                    self.sock.sendall(data + "*")
                except socket.error, arg:
                    logging.debug("抛出异常4: %s" % arg)
                    logging.info("报警的坐标%s" % data)
                time.sleep(self.sleep)
        return data

    def uwbdata(self, tag, room):
        # 生成发送数据
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        # data['pos_x'] = round(random.uniform(0.105,2.675),4)
        data['pos_y'] = round(random.uniform(0.6, 4.385), 4)

        if room == "302":
            data['pos_code'] = "0101030900"
            data['pos_x'] = round(random.uniform(0.105, 2.675), 4)

        elif room == "303":
            data['pos_code'] = "0101031000"
            data['pos_x'] = round(random.uniform(2.78, 5.35), 4)

        elif room == "304":
            data['pos_code'] = "0101031100"
            data['pos_x'] = round(random.uniform(5.455, 8.025), 4)

        elif room == "403":
            data['pos_code'] = "0101041000"
            data['pos_x'] = round(random.uniform(2.78, 5.35), 4)

        elif room == "205":
            data['pos_code'] = "0101021200"
            data['pos_x'] = round(random.uniform(8.13, 10.805), 4)

        else:
            data['pos_code'] = "0000000000"
            data['pos_x'] = round(random.uniform(8.13, 10.805), 4)

        # jsonData = json.dumps(data,sort_keys=True, indent=4, separators=(',', ': '))
        # print 'Sending0 "%s".' % jsonData
        return (data)

    def select_room(self, room_list):
        # 通过传入房间号返回房间的tag_id号
        tag_id = []
        if room_list == ['all']:
            room_list = ["302", "303", "304", "403", "205"]
        logging.info("显示的监仓有%s" % room_list)
        for room in room_list:
            if room == "302":
                tag = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            elif room == "303":
                tag = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            elif room == "304":
                tag = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
            elif room == "403":
                tag = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
            elif room == "205":
                tag = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
            else:
                print "room输入的值有误，请检查room,并重新输入"
                exit(1)
            tag_id.append(tag)

        tag = []
        for tag1 in tag_id:
            for tag2 in tag1:
                tag.append(tag2)
        print tag
        return tag

    def invalid_data(self, tag, flag):
        # 告警的异常数据生成
        data = {}
        if flag == 1:
            if tag < 12:
                room = random.choice(["303", "304", "205", "403"])

            elif tag < 24:
                room = random.choice(["302", "304", "205", "403"])

            elif tag < 36:
                room = random.choice(["303", "302", "205", "403"])

            elif tag < 48:
                room = random.choice(["303", "304", "205", "302"])

            elif tag < 60:
                room = random.choice(["303", "304", "302", "403"])

            data = self.uwbdata(tag, room)
            jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print "格式化数据111111 %s " % jsonData
        elif flag == 2:
            data = self.uwbdata(tag, "000")  # 000是为电子围栏
            jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print "格式化数据111111 %s " % jsonData
        elif flag == 3:
            jsonData = self.normal_data(tag, 1)
        # print "格式化数据111111 %s " % jsonData
        elif flag == 4:
            jsonData = 'sleep1'
        return (jsonData)

    def alarm_data(self, tag, pos_code, flag, op):
        # 生成告警消息
        # type: (object, object, object) -> object
        data = {}
        data['timestamp'] = int(time.time())  # 替换当前时间戳
        data['tag_id'] = tag
        # data['op'] = random.randint(0,1)
        data['type'] = 3
        data['pos_code'] = pos_code

        if flag == 1:
            data['warning_code'] = "0101"  # 串仓
            data['level'] = "01"
        elif flag == 2:
            data['warning_code'] = "0102"  # 电子围栏
            data['level'] = "01"
        elif flag == 3:
            data['warning_code'] = "0201"  # 卫生间滞留
            data['level'] = "02"
        elif flag == 4:
            data['warning_code'] = "0202"  # 信号失联
            data['level'] = "02"
        if op == 1:
            data['op'] = 1  # 添加告警
        elif op == 0:
            data['op'] = 0  # 取消告警
        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print "告警 %s " % jsonData
        return (jsonData)

    def normal_data(self, tag_id, flag=0):
        # 生成正常数据
        # type: (object, object) -> object
        if tag_id < 12:
            room = "302"

        elif tag_id < 24:
            room = "303"

        elif tag_id < 36:
            room = "304"

        elif tag_id < 48:
            room = "403"

        elif tag_id < 60:
            room = "205"

        data = self.uwbdata(tag_id, room)

        if flag == 1:
            data['pos_y'] = 0.5  # 厕所位置

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print jsonData
        return jsonData

    def return_room(self, data):
        # 通过pos_code返回所在的房间号
        pos_code = self.return_pos_code(data)
        if pos_code == "0101030900":
            room = "302"
        elif pos_code == "0101031000":
            room = "303"
        elif pos_code == "0101031100":
            room = "304"
        elif pos_code == "0101041000":
            room = "403"
        elif pos_code == "0101021200":
            room = "205"
        else:
            room = "000"  # 返回一个错误的值
        return (room)

    def __del__(self):
        # print "显示过的tag %s" % tag_list
        print "2222222222222222%s" % self.tag_list
        print self.G_pos_code
        for tag in self.tag_list:
            pos_code = self.G_pos_code[tag]
            print pos_code
            print tag
            data = self.alarm_data(tag, pos_code, 4, 1)
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常: %s" % arg)
            print ("信号消失告警 %s" % data)
        # print "信号消失告警,关闭进程关闭"
        self.sock.close()


room = ['302', '303', '304', '403', '205']  # 输入302，303，304，403，205 ，all或是输入单个tag标签
tag = []  # 输入单个标签为0,1,2......59,如果输入为空就会按room设置的值进行发送
count = 100  # 循环次数1次50秒左右
ip = "192.168.10.166"  # 服务器IP地址
port = 8822  # 服务器端口号
sleep = 1  # 坐标发送间隔
p = uwb(ip, port, sleep)  # 实例化类uwb
p.send_data(room, tag, count)
# p.send_alarm_data(46,2)#发送单个报警，第一个参数表示TAG,第二个表示告警级别，1是串仓，2是电子围栏，3是厕所滞留，4是信号消失。
