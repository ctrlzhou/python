#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib2,threading
import json
import time
import random
import datetime

#TSPurl="http://119.29.152.124:6268/env/dust/data/add"
TSPurl="http://192.168.10.165:6269/env/data/data/add"


def TSPSendData(Rurl,Rbody):
    #print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    headers = {'Content-Type': 'text/plain'}
    Rreq = urllib2.Request(url = Rurl,headers=headers,data =Rbody)
    Rres_data = urllib2.urlopen(Rreq)
    Rres = Rres_data.read()
    #print Rres
    time.sleep(1)

def normal_data(device,times):
    begintime = datetime.datetime.now()
    print begintime
    elstime = 0
    print "normal_data + %s" % device
    while elstime < times:
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        LAData = random.randint(40, 65)
        pm2_5Data = random.randint(50, 70)
        pm10Data = random.randint(80, 100)
        TSPonlyData = random.randint(110, 140)
        SO2Data = random.randint(5, 10)
        NO2Data = random.randint(5, 10)
        COData = random.randint(1, 5)
        O3Data = random.randint(20, 25)
        TSPData = '{"trigger_cond":"Every time","trigger_data":{"datainfo":{"data":[{"LA":' + str(\
            LAData) + '},{"pm2_5":' + str(pm2_5Data) + '},{"pm10":' + str(pm10Data) + '},{"TSP":' + str(\
            TSPonlyData) + '},{"SO2":' + str(SO2Data) + '},{"NO2":' + str(NO2Data) + '},{"CO":' + str(\
            COData) + '},{"O3":' + str(O3Data) + '}],"deviceid":"' + device[0] + '","time":"' + nowtime + '","type":' + str(\
            device[1]) + '}}}'
        print nowtime
        print TSPData
        TSPSendData(TSPurl, TSPData)
        time.sleep(3)
        endtime = datetime.datetime.now()
        print endtime
        elstime = (endtime - begintime).seconds
        print elstime

def invalid_data(device,times):
    begintime = datetime.datetime.now()
    print begintime
    elstime = 0
    print "invalid_data + %s" % device
    while elstime < times:
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        LAData = random.randint(40, 60)
        pm2_5Data = random.randint(75, 90)
        pm10Data = random.randint(100, 130)
        TSPonlyData = random.randint(150, 180)
        SO2Data = random.randint(5, 10)
        NO2Data = random.randint(5, 10)
        COData = random.randint(1, 5)
        O3Data = random.randint(20, 25)
        TSPData = '{"trigger_cond":"Every time","trigger_data":{"datainfo":{"data":[{"LA":' + str(\
            LAData) + '},{"pm2_5":' + str(pm2_5Data) + '},{"pm10":' + str(pm10Data) + '},{"TSP":' + str(\
            TSPonlyData) + '},{"SO2":' + str(SO2Data) + '},{"NO2":' + str(NO2Data) + '},{"CO":' + str(\
            COData) + '},{"O3":' + str(O3Data) + '}],"deviceid":"' + device[0] + '","time":"' + nowtime + '","type":' + str(\
            device[1]) + '}}}'
        print nowtime
        print TSPData
        TSPSendData(TSPurl, TSPData)
        time.sleep(3)
        endtime = datetime.datetime.now()
        print endtime
        elstime = (endtime - begintime).seconds
        print elstime



def send_data(deviceid,times,count):
    for num in range(0,count):
        threads = []
        for device in deviceid:
            fun = [normal_data,invalid_data]
            random_fun = random.choice(fun)
            t = threading.Thread(target=random_fun, args=(device,times,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        time.sleep(10)


deviceid = [['AABBCCAABBCC153489153489', 1],['A1B2C3A1B2C3A1B2C3123456', 1], ['AB1010106611ABCDEF202022', 1]]
times = 10
count = 1
send_data(deviceid,times,count)

