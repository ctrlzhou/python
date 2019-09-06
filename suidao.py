# -*- coding:utf8 -*-
import time,threading,socket,random,json
'''
隧道1： x = (1,31) y = (1,3)
隧道2： x = (1,31) y = (4,6)
隧道3： x = (1,31) y = (7,9) 
'''
class office():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip, port):
        server_address = (ip, port)
        print ('Connecting to %s:%s.' % server_address)
        self.sock.connect(server_address)

    def uwbdata(self,tag):
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        pos_code_list = ["010100","010200","010300","010400","010500"]
        data['pos_code'] = pos_code_list[random.randint(0,4)]
        #pos_code = pos_code_list[random.randint(0,6)]
        print data['pos_code']

        if data['pos_code'] == "010100":  # 隧道1
            data['pos_x'] = round(random.uniform(1,31), 4)
            data['pos_y'] = round(random.uniform(1.8,2.2), 4)

        elif data['pos_code'] == "010200":  # 隧道2
            data['pos_x'] = round(random.uniform(1,31), 4)
            data['pos_y'] = round(random.uniform(4.8,5.2), 4)

        elif data['pos_code'] == "010300":  # 隧道3
            data['pos_x'] = round(random.uniform(1,31), 4)
            data['pos_y'] = round(random.uniform(7.8,8.2), 4)

        elif data['pos_code'] == "010400":  # 隧道口
            data['pos_x'] = round(random.uniform(0.2,0.8), 4)
            data['pos_y'] = round(random.uniform(0.2,9.8), 4)

        elif data['pos_code'] == "010500":  # 隧道尾
            data['pos_x'] = round(random.uniform(31.2,31.8), 4)
            data['pos_y'] = round(random.uniform(0.2,9.8), 4)

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print 'Sending0 "%s".' % jsonData
        return jsonData


    def second_data(self,tag, first_data):
        #第一个正常坐标数据后发送的坐标
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        print first_data
        pos_code = self.return_pos_code(first_data)
        pos_x = float(self.return_pos_x(first_data))
        #print "xxxx",pos_x
        pos_y = float(self.return_pos_y(first_data))
        #print "yyyy", pos_y
        pos_code_list = ["010100", "010200", "010300"]
        if pos_code in pos_code_list:
            data['pos_y'] = pos_y
            data['pos_x'] = pos_x

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return jsonData


    def return_pos_code(self,data):
        code = data.split()[2]
        return code.split(",")[0]

    def return_pos_x(self,data):
        #print data.split()
        x = data.split()[4]
        return x.split(",")[0]


    def return_pos_y(self,data):
        y = data.split()[6]
        return y.split(",")[0]


    def get_coordinate(self,min, max, pos):
        # 返回当前坐标最大值和小值中间的坐标
        while (pos + 0.4 < max):
            data_pos = round(pos + random.uniform(0,0.4),4)
            pos = float(self.return_pos_x(first_data))
        else:

        if pos - 0.4 > min:
            data_pos = round(pos + random.uniform(0, 0.4), 4)
        return data_pos


    def interval_senddata(self,tag,count):
        for num in range(0,count):
            if num == 0:
                data = self.uwbdata(tag)
                self.sock.sendall(data + "*")
                print data
                time.sleep(1)
            else:
                data = self.second_data(tag,data)
                self.sock.sendall(data + "*")
                print data
                time.sleep(1.5)

    def thread_send(self,tag_id,count):
        threads = []
        for tag in tag_id:
            t = threading.Thread(target=self.interval_senddata, args=(tag,count,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

    print "多线程测试结束"
ip = "192.168.10.166"
port = 9922
count = 10000
tag_id = [0]
p = office(ip,port)
p.thread_send(tag_id,count)