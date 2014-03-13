#!/usr/local/bin/python
# -*- coding=utf-8 -*-
import sys,os,time,ConfigParser
import config
from game_update import game_update
from gener_log import gener_log

mode = sys.argv[1] # 脚本第一个参数
update_desc=sys.argv[2] # 脚本第二个参数,更新说明文件
update_file = '%s%s/%s/%s.txt' %(config.dir_config.get('execfile_log_dir'),mode,config.time_config.get('cur_mon'),\
        config.time_config.get('cur_date')) # 生成的更新文件路径
resultlog_file = '%s%s/%s/%s.txt' %(config.dir_config.get('result_log_dir'),mode,config.time_config.get('cur_mon'),\
        config.time_config.get('cur_date')) # 生成的更新文件路径
patchinfo_config = config.conf_config.get('conf_patchinfo') # 上传patchinfo.txt的配置文件
iplist_ini = config.conf_config.get('conf_iplist')  # ip信息列表
cur_date = config.time_config.get('cur_date') # 当前时间 格式:YYYY-MM-DD-HH
cur_mon = config.time_config.get('cur_mon') # 当前时间  格式:YYYY-MM


# 打印命令退出状态
def pprint_(content='',status=''):
    if status == 0:
        print content + '\x1b[1;32m\t\t[OK]\x1b[0m'
    else:
        print content + '\x1b[1;31m\t\t[Fail]\x1b[0m'
        sys.exit()

if __name__ == '__main__':
    gp = game_update(mode=mode,result_log=resultlog_file,config=config,cur_date=cur_date,cur_mon=cur_mon,\
            iplist_ini=iplist_ini,patchinfo_config=patchinfo_config,update_file=update_file)
    gp.init_dir()
    gp.get_ipaddr()
    gp.get_patchinfo()
    gl = gener_log()
    gl.GetServerUpdateList(mode,update_desc)
    server_update = gl.GenerUpdateFile(mode,update_file)
    client_update = gl.modif_patchinfo(gp)
    if server_update == 'yes' or client_update == 'yes':
        if server_update == 'yes':
            gp.stop_game()
            pprint_(content='Stop Game',status=gp.zero_.value) # 判断停服是否成功,如果不成功退出脚本
            gp.upload_execfile()
            gp.exec_update()
            pprint_(content='Update Game',status=gp.zero_.value) # 判断更新是否成功,如果不成功退出脚本
            if client_update == 'yes':
                gp.upload_patchinfo()
            if mode == 'ds-rtm' and cur_date.split('-')[3] == '08':
                print '脚本休息40分钟后继续执行'
                time.sleep(2400)
            else:
                print '脚本休息3分钟后继续执行'
                time.sleep(180)
            gp.start_game()
            pprint_(content='Start Game',status=gp.zero_.value) # 判断开服是否成功,如果不成功退出脚本
        if client_update == 'yes':
            gp.upload_patchinfo()
    else:
        # 没有任何更新,当作例维处理
        gp.stop_game()
        pprint_(content='Stop Game',status=gp.zero_.value) # 判断停服是否成功,如果不成功退出脚本
        if mode == 'ds-rtm':
            print '脚本休息40分钟后继续执行'
            time.sleep(2400)
        else:
            print '脚本休息3分钟后继续执行'
            time.sleep(180)
        gp.start_game()
        pprint_(content='Start Game',status=gp.zero_.value) # 判断开服是否成功,如果不成功退出脚本
