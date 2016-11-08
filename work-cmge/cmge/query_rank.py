#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,time
import MySQLdb as mysqldb
from MySQLdb import converters

db_host = '127.0.0.1'
db_port = '8904'
db_user = 'cmgeroot'
db_pass = 'cmgepassword'
sql1 = 'SELECT id,role_name,LEVEL FROM user_account ORDER BY LEVEL DESC LIMIT 50;'
sql2 = 'SELECT NAME,rank FROM user_pvp ORDER BY rank LIMIT 50;'
sql3 = 'SELECT a.`role_name`,l.`level` FROM user_account a,user_pve_level_info l WHERE a.id = l.`uid` ORDER BY l.level DESC LIMIT 50'
sql4 = 'show databases'
#ignore_db = ('mysql','information_schema','cmge_test','bugtracker','djangodb','bugzilla')
ignore_db = ('mysql','information_schema','cmge_test','performance_schema')
time_format = time.strftime('%Y-%m-%d',time.localtime())

def mysql_query(sql):
    conver = converters.conversions.copy()
    conver[246]=str # decimal.Decimal to str
    conver[12]=str # datatime to str
    conver[3]=str # long to str
    conver[1]=str # tinyint to str
    conver[2]=str # smallint to str
    conn = mysqldb.connect(host=db_host,port=int(db_port),user=db_user,passwd=db_pass,db=db,charset='utf8',use_unicode=False,conv=conver)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
def write_2_file(filename,data):
    file_handler = open(filename,'wb')
    for d in data:
        str_data = '\t'.join(d)
        file_handler.write(str_data+'\n')
    file_handler.close()

if __name__ == '__main__':
    db = ''
    dblist = mysql_query(sql4)
    for d in dblist:
        db = d[0]
        if db in ignore_db:
            pass
        else:
            sql1_filename = '%s/logs/%s_user-level_%s.txt' %(os.environ['HOME'],db,time_format)
            sql2_filename = '%s/logs/%s_user-pvp_%s.txt' %(os.environ['HOME'],db,time_format)
            sql3_filename = '%s/logs/%s_user-pve_%s.txt' %(os.environ['HOME'],db,time_format)
            data1 = mysql_query(sql1)
            data2 = mysql_query(sql2)
            data3 = mysql_query(sql3)
            write_2_file(sql1_filename,data1)
            write_2_file(sql2_filename,data2)
            write_2_file(sql3_filename,data3)
