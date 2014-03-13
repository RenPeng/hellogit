#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys,os,ConfigParser,time
import config
from upload_patch import upload_patch

mount_point = config.dir_config.get('mount_point')

select = None
print '当前时间为: ',time.strftime('%Y-%m-%d %H:%M:%S')
print '第一步: 游戏需要 1.更新 2.例行维护'
while not select:
    select = raw_input('请输入1或者2: ')
    if select not in ['1','2']:
        print '输入错误,请重新输入'
        select = None

if select == '1':
    update_input = None
    print '第二步: 请输入更新说明路径,例如: 版本\\1西游天下\CN.0.550.087\更新说明.txt'
    while not update_input:
        update_input = raw_input('请输入: ')
        update_desc = update_input.replace('\xe7\x89\x88\xe6\x9c\xac',mount_point).replace('\xb0\xe6\xb1\xbe',mount_point).replace('\\','/')
        update_descdir = os.path.dirname(update_desc)
        try:
            with open(update_desc) as f:
                pass
        except:
            print '不到更新说明文件"%s",请重新输入' %(update_desc)
            update_input = None
else :
    update_desc = config.script_dir + '/liwei.txt'
    # 检查更新说明文件是否存在
    try:
        with open(update_desc) as f:
            pass
    except:
        print '不到更新说明文件"%s"',update_desc
        raw_input('按回车键退出脚本')
        sys.exit()
    serverlist = []
    serverlist1 = []
    for i in config.server_map:
        serverlist.append(i)
        serverlist.sort()
    liwei_server = None
    print '第二步: 请输入要维护游戏;游戏列表如下:'
    while not liwei_server:
        for i in serverlist:
            serverlist1.append(config.server_map.get(i))
            print '\t',config.server_map.get(i)
        liwei_server = raw_input('请输入: ')
        # 检查输入是否正确:
        if liwei_server not in serverlist1:
            print '输入有误请重新输入'
            liwei_server = None
    liwei_mode = None
    print '第三步: 选择正式服还是测试服 1.正式服 2.测试服 请输入 1 或者 2'
    while not liwei_mode:
        liwei_mode = raw_input('请输入1或者2: ')
        if liwei_mode not in ['1','2']:
            print '输入有误,请重新输入'
            liwei_mode = None
    liwei_time = None
    print '第四步: 请输入例维时间\n时间格式为: YYYY-MM-DD HH:MM-SS\t例如:2013-11-12 07:30:00'
    while not liwei_time:
        liwei_time = raw_input('请输入: ')
# 检查更新说明文件是否存在

class add_crontab(object):
    def __init__(self,update_desc=update_desc,liwei_server='',liwei_mode='',liwei_time=''):
        self.update_desc = update_desc
        if liwei_server and liwei_mode and liwei_time:
            self.mode_rtm = ''
            self.mode_beta = ''
            if liwei_mode == '1':
                self.mode_rtm = 'rtm'
                self.rtm_update_time = liwei_time
            else:
                self.mode_beta = 'beta'
                self.beta_update_time = liwei_time
            self.server = liwei_server
        else:
            self.mode_rtm = ''
            self.mode_beta = ''
            choose1 = '正式服'
            rtm_server = choose1.decode('utf-8').encode('gbk')
            choose2 = '体验服'
            beta_server = choose2.decode('utf-8').encode('gbk')
            cfp = ConfigParser.ConfigParser()
            cfp.readfp(open(update_desc))
            all_sections = cfp.sections()
            for section in all_sections:
                if section == rtm_server:
                    self.mode_rtm = 'rtm'
                    self.rtm_update_time  = cfp.get(rtm_server,'更新时间'.decode('utf-8').encode('gbk'))
                elif section == beta_server:
                    self.mode_beta = 'beta'
                    self.beta_update_time = cfp.get(beta_server,'更新时间'.decode('utf-8').encode('gbk'))
            temp_list = update_desc.split('/')
            for l in temp_list:
                if config.server_map.get(l):
                    self.server = config.server_map.get(l)
    def crontab(self,mode,server,update_time):
        '''
        根据update_time,添加到计划任务
        '''
        if update_time:
            try:
                update_time_list = update_time.split()
                cron_date = update_time_list[0]
                cron_time = update_time_list[1]
                cron_date_list = cron_date.split('-')
                cron_time_list = cron_time.split(':')
                cron_month =  cron_date_list[1]
                cron_day = cron_date_list[2]
                cron_hour = cron_time_list[0]
                cron_minute = cron_time_list[1]
            except:
                print '时间格式错误,请检查'
                raw_input('按回车键退出脚本')
                sys.exit()
            file_read = open('/etc/crontab','r')
            rl = file_read.readlines()
            file_read.close()
            rl.append('%s %s %s %s * root  %s%s %s-%s %s\n' \
                %(cron_minute,cron_hour,cron_day,cron_month,config.script_dir,'/main.py',server,mode,self.update_desc))
            file_write = open('/etc/crontab','w')
            file_write.writelines(rl)
            file_write.close()
            print '-'*30
            print '任务添加成功: %s-%s 将在%s月%s日 %s点%s分 进行维护' %(server,mode,cron_month,cron_day,cron_hour,cron_minute)
            print '如果有错误,请联系运维人员(将上面一行发给运维人员即可)'
            print '-'*30
    def add_crontab(self):
        if self.mode_rtm == 'rtm':
            self.crontab(self.mode_rtm,self.server,self.rtm_update_time)
        if self.mode_beta == 'beta':
            self.crontab(self.mode_beta,self.server,self.beta_update_time)

if __name__ == '__main__':
    if select == '1':
        upload_patch(update_descdir)
        print '\n\n\n'
        liwei_server = ''
        liwei_mode = ''
        liwei_time = ''
    add = add_crontab(update_desc=update_desc,liwei_server=liwei_server,liwei_mode=liwei_mode,liwei_time=liwei_time)
    add.add_crontab()
    raw_input('按回车键退出脚本')
