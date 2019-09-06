# -*- coding:utf8 -*-
import time, threading, socket, random, json

'''
 卫生间：（0，0）－（5.45，11.655）
总经理室：（5.55，0）－（15.285，4.42）
演示厅：（5.55，4.52）－（14.966，11.655）
CTO办公室：（15.385，0）－（21.325，4.42）
财务室：（21.425,0）-(24.827,4.42)
会议室：（24.927，0）－（29.007，4.42）
办公区：（14.966，4.52）－（46.901，11.655）
'''


class office():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip, port):
        server_address = (ip, port)
        print ('Connecting to %s:%s.' % server_address)
        self.sock.connect(server_address)

    def uwbdata(self, tag):
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        pos_code_list = ["010100", "010200", "010300", "010400", "010500", "010600", "010700"]
        data['pos_code'] = pos_code_list[random.randint(0, 6)]

        if data['pos_code'] == "010100":  # 卫生间：（0，0）－（5.45，11.655）
            data['pos_x'] = round(random.uniform(0, 5.45), 4)
            data['pos_y'] = round(random.uniform(0, 11.655), 4)

        elif data['pos_code'] == "010200":  # 总经理室：（5.55，0）－（15.285，4.42）
            data['pos_x'] = round(random.uniform(5.55, 15.285), 4)
            data['pos_y'] = round(random.uniform(0, 4.42), 4)

        elif data['pos_code'] == "010300":  # CTO办公室：（15.385，0）－（21.325，4.42）
            data['pos_x'] = round(random.uniform(15.385, 21.325), 4)
            data['pos_y'] = round(random.uniform(0, 4.42), 4)

        elif data['pos_code'] == "010400":  # 财务室：（21.425, 0）-(24.827, 4.42)
            data['pos_x'] = round(random.uniform(21.425, 24.827), 4)
            data['pos_y'] = round(random.uniform(0, 4.42), 4)

        elif data['pos_code'] == "010500":  # 会议室：（24.927，0）－（29.007，4.42）
            data['pos_x'] = round(random.uniform(24.927, 29.007), 4)
            data['pos_y'] = round(random.uniform(0, 4.42), 4)

        elif data['pos_code'] == "010600":  # 演示厅：（5.55，4.52）－（14.966，11.655）
            data['pos_x'] = round(random.uniform(5.55, 14.966), 4)
            data['pos_y'] = round(random.uniform(4.52, 11.655), 4)

        elif data['pos_code'] == "010700":  # 办公区：（14.966，4.52）－（46.901，11.655）
            data['pos_x'] = round(random.uniform(14.966, 46.901), 4)
            data['pos_y'] = round(random.uniform(4.52, 11.655), 4)

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        # print 'Sending0 "%s".' % jsonData
        return jsonData

    def second_data(self, tag, first_data):
        # 第一个正常坐标数据后发送的坐标
        data = {}
        data['timestamp'] = int(time.time())
        data['tag_id'] = tag
        data['type'] = 2
        data['pos_z'] = random.randint(2, 4)
        pos_x = float(self.return_pos_x(first_data))
        pos_y = float(self.return_pos_y(first_data))

        data['pos_x'] = self.get_coordinate(0, 46.901, pos_x)

        if data['pos_x'] > 29.007:
            data['pos_y'] = self.get_coordinate(4.52, 11.655, pos_y)
        else:
            data['pos_y'] = self.get_coordinate(0, 11.655, pos_y)

        if data['pos_x'] <= 5.45:
            data['pos_code'] = "010100"
        elif 5.55 <= data['pos_x'] <= 15.285:
            if data['pos_y'] <= 4.42:
                data['pos_code'] = "010200"
            else:
                if data['pos_x'] <= 14.966:
                    data['pos_code'] = "010600"
                else:
                    data['pos_code'] = "010700"
        elif 15.385 <= data['pos_x'] <= 21.325:
            if data['pos_y'] <= 4.42:
                data['pos_code'] = "010200"
            else:
                data['pos_code'] = "010700"
        elif 21.425 <= data['pos_x'] <= 24.827:
            if data['pos_y'] <= 4.42:
                data['pos_code'] = "010400"
            else:
                data['pos_code'] = "010700"
        elif 24.927 <= data['pos_x'] <= 29.007:
            if data['pos_y'] <= 4.42:
                data['pos_code'] = "010500"
            else:
                data['pos_code'] = "010700"
        else:
            data['pos_code'] = "010700"

        jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return jsonData

    def return_pos_x(self, data):
        x = data.split()[4]
        return x.split(",")[0]

    def return_pos_y(self, data):
        y = data.split()[6]
        return y.split(",")[0]

    def get_coordinate(self, min, max, pos):
        # 返回当前坐标最大值和小值中间的坐标
        if pos + 0.4 < max:
            if pos - 0.4 > min:
                pos1 = round(pos - random.uniform(0, 0.4), 4)
                pos2 = round(pos + random.uniform(0, 0.4), 4)
                pos3 = pos
                list = [pos1, pos2, pos3]
                data_pos = list[random.randint(0, 2)]
            else:
                data_pos = round(pos + random.uniform(0, 0.4), 4)
        else:
            data_pos = round(pos - random.uniform(0, 0.4), 4)
        return data_pos

    def interval_senddata(self, tag, count):
        for num in range(0, count):
            if num == 0:
                data = self.uwbdata(tag)
                self.sock.sendall(data + "*")
                print data
                time.sleep(1)
            else:
                data = self.second_data(tag, data)
                self.sock.sendall(data + "*")
                print data
                time.sleep(1)

    def thread_send(self, tag_id, count):
        threads = []
        for tag in tag_id:
            t = threading.Thread(target=self.interval_senddata, args=(tag, count,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

    print "多线程测试结束"


ip = "192.168.10.195"
port = 9922
count = 2000
tag_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p = office(ip, port)
p.thread_send(tag_id, count)
