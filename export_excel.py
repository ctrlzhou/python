# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import xlwt
import MySQLdb

def export(host,user,password,dbname,table_name,code,start_time,end_time,outputpath):
    conn = MySQLdb.connect(host,user,password,dbname,charset='utf8')
    cursor = conn.cursor()
    sql = 'select code,pm25,pm10,no2,so2,o3,co,`timestamp` from zl_env_atmosphere_device_detail_data where code = "%s" and timelevel between "%s" and "%s" order by `timestamp` DESC' % (code,start_time,end_time)
    print sql
    count = cursor.execute(sql)
    print count
    # 重置游标的位置
    cursor.scroll(0,mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()

    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_'+table_name,cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(results)+1):
        for col in range(0,len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])

    workbook.save(outputpath)


# 结果测试
if __name__ == "__main__":
    host = "119.29.152.124"
    user = "root"
    password = "zhilu"
    dbname = "zl_env"
    table_name = "zl_env"
    code = "114403010000022000000004"
    start_time = "2018-03-16 00:00:00"
    end_time = "2018-03-16 23:00:00"
    outputpath = "datetest1.xlsx"
    export(host,user,password,dbname,table_name,code,start_time,end_time,outputpath)
