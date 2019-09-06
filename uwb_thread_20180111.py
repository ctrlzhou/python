# -*- coding:utf8 -*-
import socket, time, random, json
import threading
import logging


class uwb():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='uwb.log',
                        filemode='w')
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        logging.debug('Strange error creating socket:%s' % e)

    global tag_list
    tag_list = []

    def __init__(self, ip, port):
        global server_address
        server_address = (ip, port)
        logging.info('Connecting to %s:%s.' % server_address)
        self.sock.connect(server_address)

    def send_data(self, room, tag, count):

        try:
            if len(tag) != 0:
                if len(tag) == 1:
                    tag_id = tag[1]
                    self.single_num(count, tag_id)
                else:
                    tag_id = tag
                    self.mul_num(count, tag_id)
            else:
                tag_id = self.select_room(room)
                self.mul_num(count, tag_id)
        except socket.error, arg:
            logging.debug('获取异常 %s' % arg)

    def single_num(self, count, tag):
        global tag_list
        if tag not in tag_list:
            data = self.alarm_data(tag, 4, 0)  # 先发发送一个取消信号消失的告警
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常1 %s" % arg)
                logging.info('again Connecting to %s:%s.' % server_address)
                self.sock.connect(server_address)
            tag_list.append(tag)
        # print tag_list

        data = self.normal_data(tag)
        try:
            self.sock.sendall(data + "*")
        except socket.error, arg:
            logging.debug("抛出异常2 %s" % arg)
            logging.info('again Connecting to %s:%s.' % server_address)
            self.sock.connect(server_address)
        # print "发送正常的坐标%s" % data
        logging.info("发送报警坐标")
        self.alarm_flow(tag)
        time.sleep(10)

    def mul_num(self, count, tag_id):

        global tag_list

        for tag in tag_id:
            data = self.alarm_data(tag, 4, 0)  # 先发发送一个取消信号消失的告警
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常1 %s" % arg)
                logging.info('again Connecting to %s:%s.' % server_address)
                self.sock.connect(server_address)
            tag_list.append(tag)

        for num in range(0, count):
            self.thread_send(tag_id)
            logging.info("第%s个循环结束!" % num)

    def interval_senddata(self, tag):

        count = 19
        # global data_list
        data_list = []
        while count > 0:
            data = self.normal_data(tag)
            time.sleep(1)
            count -= 1
            # print "更新的次数%s" % count
            # data_list.append(data)
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常3: %s" % arg)
            logging.info("正常坐标%s" % data)
        # return data_list

    def thread_send(self, tag_id):
        threads = []
        logging.info("进行多线程测试%s" % tag_id)
        for tag in tag_id:
            if (tag % 10 == 0):
                t = threading.Thread(target=self.alarm_flow, args=(tag,))
                threads.append(t)
            else:
                t = threading.Thread(target=self.interval_senddata, args=(tag,))
                threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()
        # self.sock.sendall(data+"*")

    time.sleep(2)

    print "多线程测试结束"

    def alarm_flow(self, tag):
        # 该tag先发送5次正常的坐标，再发送报警
        send_data = []  # 把发送的坐标放入到列表中
        for num in range(0, 5):  # 该tag先发5次正常的值
            data = self.normal_data(tag)
            send_data.append(data)
        alarm_type = random.randint(1, 4)  # 1是串仓，2是电子围栏，3是厕所滞留
        # alarm_type = 3
        data = self.invalid_data(tag, alarm_type)  # 发送告警坐标
        send_data.append(data)
        if alarm_type != 4:
            pos_code = data[19:29]  # 获取当前告警坐标的监狱pos_code
            room = self.return_room(pos_code)  # 返回pos_code对应的room
        data = self.alarm_data(tag, alarm_type, 1)  # 发送告警
        send_data.append(data)

        for num in range(0, 10):  # 再连续发送7次告警坐标
            if alarm_type == 3:
                data = self.invalid_data(tag, alarm_type)
            elif alarm_type == 4:
                data = 'sleep1'
            else:
                jsonData = self.uwbdata(tag, room)
                data = json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            send_data.append(data)

        data = self.alarm_data(tag, alarm_type, 0)  # 取消告警
        send_data.append(data)
        data = self.normal_data(tag)  # 再发送正常坐标
        send_data.append(data)

        for data in send_data:
            if data == 'sleep1':
                time.sleep(1)
            else:
                try:
                    self.sock.sendall(data + "*")
                except socket.error, arg:
                    logging.debug("抛出异常4: %s" % arg)
                    logging.info("报警的坐标%s" % data)
            time.sleep(1)

        # print "告警TAG %s,时间是%s" % (tag,time.time())

    def uwbdata(self, tag, room):
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
        data = {}
        if flag == 1:
            if tag < 12:
                room = random.choice(["303", "304", "205", "403"])
            # print room

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

    def alarm_data(self, tag, flag, op):
        # type: (object, object, object) -> object
        data = {}
        data['timestamp'] = int(time.time())  # 替换当前时间戳
        data['tag_id'] = tag
        # data['op'] = random.randint(0,1)
        data['type'] = 3

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

    def send_alarmdata(self, tag_id, pos_code):
        if tag_id < 12:
            if pos_code != "0101030900":
                return (self.alarmdata(tag_id))
        elif tag_id < 24:
            if pos_code != "0101031000":
                return (self.alarmdata(tag_id))
        elif tag_id < 36:
            if pos_code != "0101031100":
                return (self.alarmdata(tag_id))
        elif tag_id < 48:
            if pos_code != "0101041000":
                return (self.alarmdata(tag_id))
        elif tag_id < 60:
            if pos_code != "0101021200":
                return (self.alarmdata(tag_id))
        else:
            return None

    def normal_data(self, tag_id, flag=0):
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

    def return_room(self, pos_code):
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
        for tag in tag_list:
            data = self.alarm_data(tag, 4, 1)
            try:
                self.sock.sendall(data + "*")
            except socket.error, arg:
                logging.debug("抛出异常: %s" % arg)

        print "信号消失告警 %s" % data
        # print "信号消失告警,关闭进程关闭"
        self.sock.close()


room = ['302', '303', '304', '403', '205']  # 输入302，303，304，403，205 ，all或是输入单个tag标签
tag = []  # 输入单个标签为0,1,2......59,如果输入为空就会按room设置的值进行发送
count = 1  # 循环次数
ip = "192.168.10.9"  # 服务器IP地址
port = 8822  # 服务器端口号
p = uwb(ip, port)  # 实例化类uwb
p.send_data(room, tag, count)
