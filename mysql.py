#!/usr/bin/env python
# -*- coding=utf-8 -*-
def ins_db(hostip,command,command_status,section,ser_name):
    if command != 'None':
        try:
            conn = MySQLdb.connect(host='192.168.6.193',user='kefudb',passwd='kefudb',db='test')
            cursor = conn.cursor()
            sql = "insert into test (date,servername,worldid,ser_name,hostip,exec_command,exec_status,ssh_conn_status) \
                    values(%s,%s,%s,%s,%s,%s,%s,%s)"
            param = (str(time.strftime('%Y-%m-%d')),sys.argv[1],section,ser_name,hostip,command,command_status,'ok')
            cursor.execute(sql,param)
            result = cursor.fetchone()
            conn.commit()
