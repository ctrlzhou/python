# -*- coding:UTF-8 -*-
import time
import linecache
import random
import requests
import threading
import xlrd


# {"data":[{"name":"uplink_msg","value":"{\"data_type\":259,\"data_unit\":[{\"dev_addr\":\"001-01-004-00\",\"dev_status\":3,\"dev_type\":79,\"time\":\"2019-07-01 09:36:50\"},{\"dev_addr\":\"001-01-008-00\",\"dev_status\":3,\"dev_type\":87,\"time\":\"2019-07-01 09:36:50\"}],\"terminal_mac\":\"02:00:00:31:00:23\"}\n"}]}


def send_http(count, requrl, dev_excel):
    global r
    while (count > 0):
        for i in range(1, 505):
            test_data = []
            test_data.append(uplink_dev_status(i, dev_excel))
            #test_data.append(uplink_dev_param(i,dev_excel))
            headers = {'content-type': "application/json", "Connection": "close",}
            for data in test_data:
                r = requests.post(requrl, data=data, headers=headers)
                time.sleep(1)
            print r.text
        count = count - 1
        time.sleep(1)


def add_user(num):
    username = "autotest" + str(num)
    phone = 15989891248 + num
    user_data = '{"realName": "%s", "password": "123456", "role": [52], "phone": "%s", "deptId": 390, "remarks": "","username": "%s"}' % (
        username, phone, username)
    return user_data


def thread_send(count, requrl, dev_excel_list):
    threads = []
    for dev_excel in dev_excel_list:
        t = threading.Thread(target=send_http, args=(count, requrl, dev_excel,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


def uplink_dev_up():
    data_type = 256


def uplink_dev_down():
    data_type = 257

def uplink_terminal_status():
    data_type = 261
    dev_type = 1

def uplink_dev_param(num, dev_excel):
    dev_dict = read_excel(dev_excel, num)
    terminal_mac = dev_dict["MAC"]
    data_type = 260
    dev_addr = dev_dict["dev_addr"]
    param_type = dev_dict["param_type"]
    param_value = random.randint(1, 100)
    send_data = '{"terminal_mac":"%s","data_type":%d,"data_unit":[{"param_type":%d,"dev_addr":"%s","param_value":%d}]}' % (
        terminal_mac, data_type, param_type, dev_addr, param_value)
    print send_data
    return send_data


def uplink_dev_status(num, dev_excel):
    dev_dict = read_excel(dev_excel, num)
    data_dict = {}
    data_dict['name'] = 'uplink_msg'
    data_dict['data_type'] = 259
    data_dict['dev_addr'] = dev_dict["dev_addr"]
    data_dict['dev_status'] = dev_status()
    data_dict['dev_type'] = dev_dict["dev_type"]
    data_dict['time'] = current_time()
    data_dict['terminal_mac'] = dev_dict["MAC"]
    send_data = '{"terminal_mac":"%s","data_type":259,"data_unit":[{"dev_type":%d,"dev_addr":"%s","dev_status":%d,"dev_description":"","time":"%s"}]}' % (
        data_dict['terminal_mac'], data_dict['dev_type'], data_dict['dev_addr'], data_dict['dev_status'],
        data_dict['time'])
    print send_data
    return send_data


def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()


def dev_status():
    normal_list = [0, 1, 40, 41, 42, 43, 44, 180, 181, 190, 191, 192, 193, 195, 196, 200, 201, 208, 213, 214, 231, 233,
                   234, 235, 237, 239, 240, 241, 242, 243, 244, 245, 246, 247, 205, 72, 73]
    action_list = [78, 151, 152, 154, 202, 209, 210, 76, 77, 70, 74, 75, 3, 4, 7]
    fault_list = [6, 21, 22, 23, 24, 162, 165, 206, 211, 212, 230, 232, 234, 160, 161, 71, 153, 163, 164, 236]
    police_list = [2, 150, 5, 207, 220, 221, 222, 223, 224, 225, 226, 227, 228, 238]
    normal = random.choice(normal_list)
    action = random.choice(action_list)
    fault = random.choice(fault_list)
    police = random.choice(police_list)
    status_list = [normal, action, fault, police]
    status = int(random.choice(status_list))
    return status


def dev_addr():
    Channel_number = "00"
    with open('Channel_number.txt', 'w') as single_Channel_number:
        for i in range(1, 11):
            Controller_number = str(i).zfill(3)
            for k in range(1, 11):
                Loop_number = str(k).zfill(2)
                for j in range(1, 256):
                    Address_number = str(j).zfill(3)
                    dev_addr = Controller_number + "-" + Loop_number + "-" + Address_number + "-" + Channel_number
                    print dev_addr
                    single_Channel_number.write(dev_addr + '\n')


def read_excel(dev_excel, num):
    xls_file = xlrd.open_workbook(dev_excel)
    xls_sheet = xls_file.sheet_by_name("sheet1")
    #Loop_number = str(int(xls_sheet.cell_value(num, 14))).zfill(2)  # 14列是回路号
    #Channel_number = str(int(xls_sheet.cell_value(num, 15))).zfill(3)  # 15列是通道号
    #Controller_number = str(int(xls_sheet.cell_value(num, 20))).zfill(3)  # 20列是控制器号
    dev_dict = {}
    #dev_dict["dev_addr"] = Controller_number + "-" + Loop_number + "-" + Channel_number + "-" + "00"
    dev_dict["dev_addr"]= str(xls_sheet.cell_value(num, 5))
    # print dev_addr
    dev_dict["MAC"] = str(xls_sheet.cell_value(num, 20))  # 22列是传输装置的MAC
    # print MAC
    dev_dict["dev_type"] = int(xls_sheet.cell_value(num, 21))  # 23列是设备类型
    # print dev_value
    dev_dict["param_type"] = int(xls_sheet.cell_value(num, 22))  # 24列是参数类型
    return dev_dict


def current_time():
    timedata = time.localtime(time.time())
    # print timedata
    # print timedata
    year = timedata.tm_year
    year = str(year).zfill(2)
    mon = str(timedata.tm_mon).zfill(2)
    day = str(timedata.tm_mday).zfill(2)
    hour = str(timedata.tm_hour).zfill(2)
    min = str(timedata.tm_min).zfill(2)
    sec = str(timedata.tm_sec).zfill(2)  # 不足2位前面补0

    data = year + "-" + mon + "-" + day + " " + hour + ":" + min + ":" + sec
    return data


def terminal_mac():
    with open('mac.txt', 'w') as single_mac:
        mac_head = "00:01:02:03:04"
        for i in range(0, 256):
            n = str(hex(i)[2:]).zfill(2)
            print mac_head + ":" + n
            mac = mac_head + ":" + n
            single_mac.write(mac + '\n')

def NB_devices_status():
    status_list = ['ALARM','FAULT','BATFAULT','NORMAL','LOSE','WARN','KEYTEST','OPEN','CLOSE','START','LOGIN','LOGOUT','MPFAULT','BTFAULT','RELOST','REFAULT']
    dev_status = random.choice(status_list)
    data = '{"data_type": 701,"dev_id": "111111","dev_status": "%s","dev_type": "NBSMOKE"}' % dev_status
    print data
    return data


def NB_devices_httpsend(requrl):
    for i in range(0,500):
        data = NB_devices_status()
        headers = {'content-type': "application/json", "Connection": "close", }
        r = requests.post(requrl, data=data, headers=headers)
        time.sleep(1)
        print r.text

#requrl = "http://192.168.10.250/rest/monitor/data/report"
#requrl = "http://139.159.159.241:8080/rest/monitor/data/report"
requrl = "http://firecontrol.zhilutec.com/rest/monitor/data/report"
#count = 100000
#dev_excel_list = ["dev_listB.xls", "dev_listC.xls", "dev_listD.xls", "dev_listE.xls"]
#dev_excel_list = ["BAIDUA.xls","BAIDUB.xls"]
#thread_send(count, requrl, dev_excel_list)
NB_devices_httpsend(requrl)