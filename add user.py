# -*- coding:UTF-8 -*-
import requests


def send_http(requrl, num,Author):
    for i in range(1, num):
        test_data = add_user(i)
        headers = {'content-type': "application/json", 'Authorization': Author}
        r = requests.post(requrl, data=test_data, headers=headers)
        print r.text


def add_user(num):
    username = "autotest" + str(num)
    phone = 15989891248 + num
    user_data = '{"realName": "%s", "password": "123456", "role": [38], "phone": "%s", "deptId": 15245, "remarks": "","username": "%s"}' % (
        username, phone, username)
    return user_data


def uplink_send(requrl):
    for i in range(1, 2):
        test_data = send_param()
        headers = {'content-type': "application/json"}
        r = requests.post(requrl, data=test_data, headers=headers)
        print r.text


def send_param():
    terminal_mac = "00:01:02:03:04:05"
    data_type = 260
    dev_addr = "003-01-213-00"
    param_type = 21
    param_value = 100
    send_data = '{"terminal_mac":"%s","data_type":260,"data_unit":[{"param_type":%d,"dev_addr":"%s","param_value":%d}]}' % (
        terminal_mac, param_type, dev_addr, param_value)
    print send_data
    return send_data


def dev_addr(requrl, num):
    Channel_number = "00"
    for i in range(5, 11):
        Controller_number = str(i).zfill(3)
        for k in range(1, 11):
            Loop_number = str(k).zfill(2)
            for j in range(1, 256):
                Address_number = str(j).zfill(3)
                dev_addr = Controller_number + "-" + Loop_number + "-" + Address_number + "-" + Channel_number
                num = num - 1
                if num == 0:
                    break
                print dev_addr
                add_dev(dev_addr, num, requrl)


def add_dev(dev_addr, num, requrl):
    data = '{"buildingId": 14486,"unitId": 14482,"parentId": 1,"number": %s,"subsystem": "1","type": "37","brand": 4,"series": 7,\
    "floor": "1", "location": "电线%d", "room": "101", "installDate": "2019-07-01 00:00:00", "name": "缆式线型感温火灾探测器"}' % (dev_addr,num)
    headers = {'content-type': "application/json", 'Authorization': "Bearer 82a0a21c-23f8-486c-8d66-a76214ed7d5f"}
    r = requests.post(requrl, data=data, headers=headers)
    print r.text

#requrl = "http://139.159.159.241:8080/rest/admin/user"
requrl = "http://192.168.10.250/rest/admin/user"
#requrl = "http://192.168.10.250/rest/pub/device"
#requrl = "http://139.159.159.241:8080/rest/admin/user"
#requrl = "http://192.168.10.250/rest/monitor/data/report"
num = 5001
Author="Bearer fade4c63-03ef-46b8-9d2c-bdaeaa1294c2"
send_http(requrl, num,Author)
