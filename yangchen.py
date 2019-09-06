# -*- coding:utf8 -*-
import random, time, MySQLdb


# if sys.getdefaultencoding() != 'utf-8':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

def add_data():
    data = {}
    min_time = 1488297600  # 2017-3-1
    max_time = 1514044800 #2017-12-24
    db = MySQLdb.connect("119.29.152.124", "root", "zhilu", "zl_env",charset="utf8")
    cursor = db.cursor()

    while min_time < max_time:
        timestamp = min_time
        timelevel = min_time + 86400
        data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        data['timelevel'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timelevel))
        min_time += 86400
        data['code'] = 342
        data['name'] = '赛百诺二期'
        data['tsp'] = random.randint(150, 200)
        data['la'] = random.randint(40, 60)
        data['pm10'] = random.randint(100, 150)
        data['pm25'] = random.randint(80, 100)
        data['duration'] = 0
        data['maxduration'] = random.randint(30, 60)
        data['accduration'] = random.randint(180, 240)
        data['standard'] = random.randint(400, 600)
        data['unstandard'] = random.randint(200, 400)
        data['standardper'] = round(random.uniform(85, 99), 2)

        sql = "insert into zl_env_dust_project_day_data_history(code,name,timestamp,timelevel,tsp,la,pm10,pm25,duration,maxduration,accduration,standard,unstandard,standardper) values\
         (%s,'%s','%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%f)" % (data['code'], data['name'], data['timestamp'], data['timelevel'], data['tsp'], data['la'],data['pm10'], data['pm25'], data['duration'] \
          , data['maxduration'], data['accduration'], data['standard'], data['unstandard'], data['standardper'])
        print sql
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            print "添加数据库失败"
    db.close()


add_data()
