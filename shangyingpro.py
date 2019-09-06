# -*-coding:utf-8 -*-
import random
import subprocess
import threading
import time
import requests


def send_data(count, data):
    for j in range(0, count):
        for i in range(1, 256):
            status = dev_status()
            mac = data[1]
            number = data[0]
            print mac
            print number
            main = "F:\pythoncode\syeptest\syeptest.exe  -LP 10001 -H 123.207.39.248 -P 9000 -D 00:11:22:33:11:16" \
                   " -F -t connect -F -t status1 -a %s%d-0 -dt 79 -ds %d -des autotest -E" % (number, i, status)
            main = "F:\pythoncode\syeptest\sydoc2013.exe -H 123.207.39.248 -P 9001 -D %s" \
                   " -F -t dev_status -st 1 -sa 01 -dt 24 -da %s%d-0 -ds %d -dsdesc autotest -E" % (mac, number, i, status)
            print main
            cmd = subprocess.Popen(main, shell=True)
            cmd.wait()
            print("-" * 50, "ending", "-" * 50)
            print(cmd.poll())
            cmd.kill()
            cmd.terminate()
            print(cmd.pid)


def thread_send(count, number_list):
    threads = []
    for data in number_list:
        print data
        t = threading.Thread(target=send_data, args=(count, data))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


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

def NB_devices_status(device_num):
    status_list = ['ALARM','FAULT','BATFAULT','NORMAL','LOSE','WARN','KEYTEST','OPEN','CLOSE','START','LOGIN','LOGOUT','MPFAULT','BTFAULT','RELOST','REFAULT','KEYTEST']
    dev_status = random.choice(status_list)
    eventTime = current_time()
    data = '{"notifyType":"deviceDataChanged","deviceId":"055d9c93-ef90-408b-9d3f-6971fd36b8dd","gatewayId":"055d9c93-ef90-408b-9d3f-6971fd36b8dd",' \
           '"requestId":null,"service":{"serviceId":"alarmreport","serviceType":"alarmreport","data":{"length":32,"valuestring":' \
           '"NBSMOKE:%d,%s"},"eventTime":"%s"}}' %(device_num,dev_status,eventTime)
    return data

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

    data = year + mon + day + "T" + hour + min + sec + "Z"
    return data

def NB_devices_param(device_num):
    DSOC = str(random.randint(50,100)).zfill(3)
    BSOC = str(random.randint(50,100)).zfill(3)
    num   = random.randint(1,100)
    if num > 50:
        status = "ALARM"
    else:
        status = "NORMAL"
    SM = str(num).zfill(3)
    eventTime = current_time()
    device_num = device_num
    data = '{"notifyType":"deviceDataChanged","deviceId":"055d9c93-ef90-408b-9d3f-6971fd36b8dd","gatewayId":"055d9c93-ef90-408b-9d3f-6971fd36b8dd"' \
           ',"requestId":null,"service":{"serviceId":"uploaddevs","serviceType":"uploaddevs","data":{"length":32,"datastring":"NBSMOKE:%s, ' \
           '%s,-DSOC/%s,-BSOC/%s,-SM/%s"},"eventTime":"%s"}}' %(device_num,status,DSOC,BSOC,SM,eventTime)
    return data

def NB_devices_httpsend(number,requrl,count):
    for k in range(0,count):
        for i in range(0,101):
            number = int(number)
            device_num = number + i
            data_list =[NB_devices_status(device_num),NB_devices_param(device_num)]
            data = random.choice(data_list)
            print data
            headers = {'content-type': "application/json", "Connection": "close", }
            r = requests.post(requrl, data=data, headers=headers)
            time.sleep(1)
            print r.text

def thread_httpsend(number_list,requrl,count):
    threads = []
    for number in number_list:
        t = threading.Thread(target=NB_devices_httpsend, args=(number, requrl,count,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


mac7 = "00:00:00:00:11:12"
mac6 = "00:11:22:33:11:16"
mac5 = "00:11:22:33:11:14"
number_list = [["5-1-", mac5], ["5-2-", mac5], ["6-1-", mac6], ["6-2-", mac6], ["7-1-", mac7], ["7-2-", mac7]]
count = 100
thread_send(count, number_list)
#number_list =[10000,20000,30000,40000,50000,60000,70000,80000,90000,11000,21000,31000,41000,51000,61000,71000,81000,91000]
#number_list =[10000,20000,30000,40000,50000,60000,70000,80000,90000]
url = "http://123.207.39.248:9300/SY_NBIOT"
#thread_httpsend(number_list,url,count)