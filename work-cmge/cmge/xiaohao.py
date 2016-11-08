#!/usr/bin/env python
# -*- coding=utf-8 -*-

import re,time,os,sys
mgs_log_dir = '/data/mgs_log'
#yesterday = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
yesterday = sys.argv[1]
logfile_pattern = r'wh_100_user_log_%s_server' % yesterday
date_pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}:[0-9]{2}\$\$"
yuanbao_xiaohao = (r"REMOVE_I_MONEY",'%s/xiaohao_%s.txt' %(os.environ['HOME'],yesterday))
meinv_chongxing = (r"PATRONIZE",'%s/chongxing_%s.txt' %(os.environ['HOME'],yesterday))
pvp_rank = (r"RANK_PVP",'%s/pvp_%s.txt' %(os.environ['HOME'],yesterday))

def analysis_yuanbao(log_file_handler,pattern,result_file_handler):
    row = True
    while row:
        row = log_file_handler.readline()
        match = re.search(date_pattern+pattern,row)
        if match:
            cost_list = row.split('$$')
            uid = cost_list[2]
            cost = int(cost_list[-3]) - int(cost_list[-2])
            cost_reason = cost_list[-1].replace('\n','')
            result_file_handler.write("%s\t%s\t%d\t%s\n"%(server_id,uid,cost,cost_reason))
def analysis_chongxing(log_file_handler,pattern,result_file_handler):
    row = True
    item_dict = {1:'学识',2:'美女卡片',3:'兵法碎片',4:'皇子'}
    while row:
        row = log_file_handler.readline()
        match = re.search(date_pattern+pattern,row)
        if match:
            chongxin_list = row.split('$$')
            uid = chongxin_list[2]
            beauty_id = chongxin_list[4]
            beauty_name = chongxin_list[4]
            geted_item = int(chongxin_list[-2])
            geted_item_num = chongxin_list[-1].replace('\n','')
            result_file_handler.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(server_id,uid,beauty_id,beauty_name,geted_item,geted_item_num))
def analysis_pvp(log_file_handler,pattern,result_file_handler):
    row = True
    pvp_result_dict = {0:'挑战失败',1:'挑战成功'}
    while row:
        row = log_file_handler.readline()
        match = re.search(date_pattern+pattern,row)
        if match:
            pvp_list = row.split('$$')
            uid = pvp_list[2]
            pvp_from_rank =  pvp_list[3]
            pvp_to_rank = pvp_list[4]
            pvp_result = int(pvp_list[-1].replace('\n',''))
            result_file_handler.write("%s\t%s\t%s\t%s\t%s\n"%(server_id,uid,pvp_from_rank,pvp_to_rank,pvp_result))

if __name__ == '__main__':
    file_list = os.listdir(mgs_log_dir)
    for filename in file_list:
        if re.search(logfile_pattern,filename):
            log_file = os.path.join(mgs_log_dir,filename)
            server_id = log_file.split('_')[-1]
            file_handler = open(log_file)
            analysis_yuanbao(file_handler,yuanbao_xiaohao[0],open(yuanbao_xiaohao[1],'ab'))
            file_handler = open(log_file)
            analysis_chongxing(file_handler,meinv_chongxing[0],open(meinv_chongxing[1],'ab'))
            file_handler = open(log_file)
            analysis_pvp(file_handler,pvp_rank[0],open(pvp_rank[1],'ab'))
