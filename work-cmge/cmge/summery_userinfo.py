#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os,sys,time
import MySQLdb as mysqldb
from zipfile import ZipFile as ZF
from file_upload import create_sftp

# Config  Begin
db_host = '127.0.0.1'
db_port = 8904
db_user = 'cmgeroot'
db_pass = 'cmgepassword'
ignore_db = ('mysql','information_schema','cmge_test')
# SQL
base_item_number_sql = "SELECT  a.id,COUNT(a.id) FROM user_account AS a LEFT JOIN %s AS b  ON a.id = b.uid  \
			WHERE b.id IS NOT NULL  GROUP BY a.id"
beauty_number_sql = base_item_number_sql % "user_beauty"
officer_number_sql = base_item_number_sql % "user_officer"
prince_number_sql = base_item_number_sql % "user_prince"

base_itemid_number_sql = "SELECT  a.id,b.%s as item_id,COUNT(b.%s) FROM user_account AS a LEFT JOIN %s AS b  ON a.id = b.uid \
			WHERE b.uid IS NOT NULL GROUP BY id,item_id"
beauty_id_sql = base_itemid_number_sql % ("beauty_id","beauty_id","user_beauty")
officer_id_sql = base_itemid_number_sql % ("card_id","card_id","user_officer")
equipment_id_sql = base_itemid_number_sql % ("equip_id","equip_id","user_equipment")
prince_id_sql = base_itemid_number_sql %("id","id","user_prince")

# 添加字段不要在最后2个,后面要转换时间格式
user_info_sql = "SELECT id,id,name,server_id,platform_id,channel,role_name,level,gold,silver,register_time,login_time FROM user_account"
show_all_tables = "SHOW FULL TABLES WHERE table_type = 'BASE TABLE'"
show_db = "show databases"
# Config END

def mysql_query(sql):
    conn = mysqldb.connect(host=db_host,port=int(db_port),user=db_user,passwd=db_pass,db=db,charset='utf8',use_unicode=False)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
def calc_item_num(sql):
    result_data = mysql_query(sql)
    tmp_dict = {}
    for d in result_data:
        if d[0] in tmp_dict:
            # uid:item_number
            tmp_dict[d[0]].append(d[1])
        else:
            tmp_dict[d[0]] = [d[1]]
    return tmp_dict
def calc_itemid_num(sql):
    result_data = mysql_query(sql)
    tmp_dict1 = {}
    tmp_dict2 = {}
    for d  in result_data:
        # {uid:{tem_id:number,item_id:number},uid....}
        if d[0] not in tmp_dict1 and len(tmp_dict1) != 0:
            tmp_dict2 = {}
            tmp_dict2[d[1]] = d[2]
        else:
            tmp_dict2[d[1]] = d[2]
        tmp_dict1[d[0]] = tmp_dict2
    return tmp_dict1
def format_itemid_num(uid,data):
    keys = data[uid].keys()
    item_num = []
    for key in keys:
        item_num.append(str(int(key))+','+str(int(data[uid][key])))
    return item_num
def summery_user_info():
    file_handler = open(filename,'ab')
    # Exec sql
    print '\tCacl user data from %s........' % db
    user_base_info = mysql_query(user_info_sql)
    beaauty_num_dict = calc_item_num(beauty_number_sql)
    office_num_dict = calc_item_num(officer_number_sql)
    prince_num_dict = calc_item_num(prince_number_sql)

    beauty_itemid_num = calc_itemid_num(beauty_id_sql)
    officer_itemid_num = calc_itemid_num(officer_id_sql)
    prince_itemid_num = calc_itemid_num(prince_id_sql)
    equip_itemid_num= calc_itemid_num(equipment_id_sql)
    print '\tWrite result to file.....'
    for base_info in user_base_info:
        user_id = base_info[0]
        user_others = list(base_info[1:])
        # summery user item numbers
        beauty_num = ['美女,']+[0]
        office_num = ['名臣,']+[0]
        prince_num = ['皇子,']+[0]
        if user_id in beaauty_num_dict:
            beauty_num = ['美女,']+beaauty_num_dict[user_id]
        if user_id in office_num_dict:
            office_num = ['名臣,']+office_num_dict[user_id]
        if user_id in prince_num_dict:
            prince_num = ['皇子,']+prince_num_dict[user_id]
        # summery user items ids
        beauty_id = [' ']
        officer_id = [' ']
        prince_id = [' ']
        equip_id = [' ']
        if user_id in beauty_itemid_num:
            beauty_id = format_itemid_num(user_id,beauty_itemid_num)
        if user_id in officer_itemid_num:
            officer_id = format_itemid_num(user_id,officer_itemid_num)
        if user_id in prince_itemid_num:
            prince_id = format_itemid_num(user_id,prince_itemid_num)
        if user_id in equip_itemid_num:
            equip_id = format_itemid_num(user_id,equip_itemid_num)
        # user basic information
        tmp_list = []
        for i in xrange(len(user_others)):
            try:
                str_field = str(int(user_others[i]))
            except:
                str_field = user_others[i]
            tmp_list.append(str_field)
        utc_time1 = tmp_list[-1]
        utc_time2 = tmp_list[-2]
        t = lambda x: time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(x)))
        hummen_time1 = t(utc_time1)
        hummen_time2 = t(utc_time2)
        tmp_list[-1] = hummen_time1
        tmp_list[-2] = hummen_time2
        userinfo = '\t'.join(tmp_list)
        # items id info
        str_equip_id =  ';'.join(equip_id)
        str_beauty_id = ';'.join(beauty_id)
        str_officer_id = ';'.join(officer_id)
        str_prince_id = ';'.join(prince_id)

        str_beauty_num = beauty_num[0]+str(int(beauty_num[1]))
        str_officer_num = office_num[0]+str(int(office_num[1]))
        str_prince_num = prince_num[0]+str(int(prince_num[1]))
        str_all_items_num = str_beauty_num + ';' + str_officer_num +';' + str_prince_num
	# write to file 
        file_handler.write('%s\t%s\t%s\t%s\t%s\t%s\n' %(userinfo,str_all_items_num,str_beauty_id,str_officer_id,str_prince_id,str_equip_id))
    file_handler.close()

def calc_md5(filename):
    try:
        from hashlib import md5
    except:
        import md5
    md = md5()
    md.update(open(filename).read())
    md5_value = md.hexdigest()
    md5_file = filename.replace('.txt','.md5')
    md5_filehandler = open(md5_file,'ab')
    md5_filehandler.write(md5_value)
    md5_filehandler.close()
    print 'All result write to %s is done' % md5_file

if __name__ == '__main__':
    today = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    today_1 = time.strftime('%Y-%m-%d',time.localtime())
    filename = '/data/user_info/wh_100_user_info_%s.txt' % today
    db = ''
    db_list = mysql_query(show_db)
    for d in db_list:
        db = d[0]
        if db in ignore_db:
            pass
        else:
            summery_user_info()
    create_sftp(filename,'/data/user_info/118.192.76.176')
