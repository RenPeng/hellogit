#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,time
import MySQLdb as mysqldb
from MySQLdb import converters

db_host = '127.0.0.1'
db_port = '8904'
db_user = 'cmgeroot'
db_pass = 'cmgepassword'
sql2 = "SELECT channel,COUNT(*) FROM user_account WHERE FROM_UNIXTIME(register_time) >= '%s' group by channel"
sql4 = 'show databases'
#ignore_db = ('mysql','information_schema','cmge_test','bugtracker','djangodb','bugzilla')
ignore_db = ('mysql','information_schema','cmge_test')
time_format = time.strftime('%Y-%m-%d',time.localtime())
conver_db = {'cmge_1':'一服','cmge_2':'二服','cmge_3':'三服','cmge_4':'混服一区','cmge_5':'混服二区'}
channel_id = {3:'91越狱',1:'中手游正版',4:'中手游WEB',5:'中手游WAP',6:'PP',7:'ITools',8:'快用',9:'同步推',50:'win32',20:'中手游安卓',21:'360安卓',22:'91安卓',23:'豌豆荚',24:'多酷',25:'小米',26:'UC',27:'安智',28:'联想',29:'oppo',30:'当乐',31:'步步高【vivo】',32:'华为',10:'中手游伪正版',11:'爱思'}
channel_keys = channel_id.keys()

def mysql_query(sql):
    conver = converters.conversions.copy()
    conver[246]=str # decimal.Decimal to str
    conver[12]=str # datatime to str
    conver[3]=str # long to str
    conver[8]=str # long to str
    conver[1]=str # tinyint to str
    conver[2]=str # smallint to str
    conn = mysqldb.connect(host=db_host,port=int(db_port),user=db_user,passwd=db_pass,db=db,charset='utf8',use_unicode=False,conv=conver)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

if __name__ == '__main__':
    db = ''
    channel_dict = {}
    for key in channel_keys:
        channel_dict[str(key)] = 0
    dblist = mysql_query(sql4)
    for d in dblist:
        db = d[0]
        if db in ignore_db:
            pass
        else:
            sql_account = sql2 %time_format
            account_result = mysql_query(sql_account)
            for i in account_result:
                channel_dict[i[0]] += int(i[1])
    file = 'newadd.txt'
    file_handler = open(file,'wb')
    for key in channel_keys:
        file_handler.write(channel_id[key] + '\t' + str(channel_dict[str(key)])+'\n')
