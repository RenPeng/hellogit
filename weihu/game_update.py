#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys,os,ssh,ConfigParser,time
from multiprocessing import Process,Value

class game_update(object):
    def __init__(self,mode='',result_log='',config='',cur_date='',cur_mon='',\
            iplist_ini='',patchinfo_config='',update_file=''):
        '''
        if mode.split('-')[1] == 'rtm':
            server = '正式服'.decode('utf-8').encode('gbk')
        elif mode.split('-')[1] == 'beta':
            server = '体验服'.decode('utf-8').encode('gbk')
        else:
            sys.exit('在更新说明中找不到与%s对应的配置',mode.split('-')[1])
            '''
        self.mode = mode
        self.config = config
        self.result_log = result_log
        self.cur_date = cur_date 
        self.cur_mon = cur_mon 
        self.iplist_ini = iplist_ini
        self.patchinfo_config = patchinfo_config
        self.update_file = update_file
        self.local_time = int(str(time.time()).split('.')[0])
        # 停服命令
        self.stop_command = 'cd /data/'  + self.mode.split('-')[0] + 'GameServer/Server && ./stop.sh'
        self.stop_command_time = 'cd /data/'  + self.mode.split('-')[0] + 'GameServer_time/Server && ./stop.sh'
        # 开服命令
        self.start_command = 'cd /data/' + self.mode.split('-')[0] + 'GameServer/Server && ./run.sh'
        self.start_command_time = 'cd /data/' + self.mode.split('-')[0] + 'GameServer_time/Server && ./run.sh'
        # 执行更新命令
        self.update_command = '/bin/sh ' + cur_date
    def init_dir(self):
        '''
        初始化脚本使用的目录,目录结构如下:
        ./conf         # 配置文件目录
        ./result_log   # 记录更新日志产生的的日志
        ./update_log   # 存放patchinfo文件和更新日志
        '''
        if not os.path.isdir(self.config.dir_config.get('result_log_dir') + self.mode + os.sep  + self.cur_mon):
            os.makedirs(self.config.dir_config.get('result_log_dir') + self.mode + os.sep + self.cur_mon)
        if not os.path.isdir(self.config.dir_config.get('conf_dir')):
            os.makedirs(self.config.dir_config.get('conf_dir'))
        if not os.path.isdir(self.config.dir_config.get('execfile_log_dir') + self.mode + os.sep + self.cur_mon):
            os.makedirs(self.config.dir_config.get('execfile_log_dir') + self.mode +os.sep +self.cur_mon)
    def get_ipaddr(self):
        '''
        获取ip列表,用户名,密码
        '''
        ip_par = ConfigParser.ConfigParser()
        ip_par.readfp(open(self.iplist_ini))
        self.user_ip=ip_par.get(self.mode,'username')
        self.pass_ip=ip_par.get(self.mode,'password')
        self.port_ip=int(ip_par.get(self.mode,'port'))
        self.all_addr = []
        self.all_option = ip_par.options(self.mode)
        self.all_option.remove('username')
        self.all_option.remove('password')
        self.all_option.remove('port')
        for option in self.all_option:
            self.all_addr.append(ip_par.get(self.mode,option)+':'+option)
    def get_patchinfo(self):
        '''
        获取上传patchinfo文件的主机信息,用户名密码等信息
        '''
        cfp_patch = ConfigParser.ConfigParser()
        cfp_patch.readfp(open(self.patchinfo_config))
        self.addr_patch = cfp_patch.get(self.mode,'address')
        self.port_patch = cfp_patch.get(self.mode,'port')
        self.user_patch = cfp_patch.get(self.mode,'username')
        self.pass_patch= cfp_patch.get(self.mode,'password')
        self.local_file = cfp_patch.get(self.mode,'local_file')
        self.remote_path = cfp_patch.get(self.mode,'remote_path')
        self.use_ssl = cfp_patch.get(self.mode,'use_ssl')
    def upload_patchinfo(self):
        '''
        上传patchinfo文件        
        '''
        import ftplib
        if self.use_ssl == 'no':
            ftp = ftplib.FTP()
        else:
            ftp = ftplib.FTP_TLS()
        rtm_list = ['xytx_sdo','xytx_rtm','xytx_ogame','xytx_fhgame']
        for addr in self.addr_patch.split(','):
            ftp.connect(host=addr,port=self.port_patch)
            ftp.login(user=self.user_patch,passwd=self.pass_patch)
            file_name = os.path.basename(self.local_file)
            if self.mode == 'xytx-rtm':
                for i in rtm_list:
                    ftp.cwd(i)
                    file_object = open(self.local_file)
                    ftp.storbinary('STOR %s%s%s' %('patchinfo_',i.split('_')[1],'.txt'),file_object)
                    ftp.cwd('/')
                    file_object.close()
            else:
                ftp.cwd(self.remote_path)
                file_object = open(self.local_file)
                ftp.storbinary('STOR %s' %file_name,file_object)
                file_object.close()
            ftp.quit

    def write_log(self,command_output='',hostname='',hostid='',comm_name=''):
        '''
        将服务器返回的输出,写入到文件中
        '''
        self.init_dir()
        log_file = open(self.result_log,'ab')
        log_file.write("%s [%s:%s:%s] %s %s %s" %('-'*20,hostid,hostname,self.mode,'Start','-'*20,'\n'))
        log_file.write(comm_name+'\n')
        log_file.write('\t' + command_output)
        log_file.write("%s [%s:%s:%s] %s %s %s" %('-'*20,hostid,hostname,self.mode,'End','-'*20,'\n'))
        log_file.close()
    def stop_game(self):
        ''' 执行停服命令 '''
        if self.mode == 'ds-beta' or self.mode == 'xyol-beta':
            self.luncher(command=['date +%s',self.stop_command_time,self.stop_command],file='')
        else:
            self.luncher(command=self.stop_command,file='')
    def start_game(self):
        ''' 执行开服命令 '''
        if self.mode == 'ds-beta' or self.mode == 'xyol-beta':
            self.luncher(command=['date +%s',self.start_command_time,self.start_command],file='')
        else:
            self.luncher(command=self.start_command,file='')
    def exec_update(self):
        ''' 执行更新 '''
        self.luncher(command=self.update_command,file='')
    def upload_execfile(self):
        ''' 把需要执行的命令,存放在一个文件中,通过 /bin/sh file 执行更新 '''
        try:
            a = open(self.update_file)
        except:
            raise IOError('Can\'t open ' + self.update_file)
        file_handler = a.readlines()
        self.luncher(command='',file=file_handler)
    def luncher(self,command='',file=''):
        ''' 根据主机列表'all_addr'的长度产生相应数量的进程,并调用connector方法执行ssh连接 '''
        self.zero_ = Value('i',0)
        luncher_box = []
        for s in xrange(len(self.all_addr)):
            hostip = self.all_addr[s].split(':')[0]
            hostid = self.all_addr[s].split(':')[1]
            arguments = (hostip,hostid,command,file,self.zero_)
            luncher_box.append(Process(target=self.connector,args=(arguments)))
        for p in xrange(len(luncher_box)):
            luncher_box[p].start()
        for j in xrange(len(luncher_box)):
            luncher_box[j].join(20)
    def connector(self,args1,args2,args3,args4,args5):
        ''' 执行ssh连接; 根据参数不同,决定是执行命令或者是上传需要执行的更新文件 '''
        hostip = args1
        hostid = args2
        command = args3
        exec_file = args4
        sclient = ssh.SSHClient()
        sclient.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sclient.connect(hostname=hostip,port=self.port_ip,username=self.user_ip,password=self.pass_ip,timeout=40)
        if exec_file == '':
            #if command == self.update_command:
            #    chan.get_pty()
            if command[0] == 'date +%s':
                chan = sclient.get_transport().open_session()
                chan.exec_command(command[0])
                utc_time = chan.recv(11)
                result = int(utc_time[0:-1])
                if result-600 < self.local_time < result+600:
                    chan = sclient.get_transport().open_session()
                    out = chan.makefile()
                    chan.exec_command(command[2])
                    command_status = int(chan.recv_exit_status())
                    self.write_log(command_output=out.read(),hostname=hostip,hostid=hostid,comm_name=command[2])
                else:
                    chan = sclient.get_transport().open_session()
                    out = chan.makefile()
                    chan.exec_command(command[1])
                    command_status = int(chan.recv_exit_status())
                    self.write_log(command_output=out.read(),hostname=hostip,hostid=hostid,comm_name=command[1])
            else:
                chan = sclient.get_transport().open_session()
                if command == self.update_command:
                    chan.get_pty()
                out = chan.makefile()
                chan.exec_command(command)
                command_status  = int(chan.recv_exit_status())
                self.write_log(command_output=out.read(),hostname=hostip,hostid=hostid,comm_name=command)
            args5.value += command_status
        else:
            sftp = sclient.open_sftp()
            sftp_file = sftp.file(self.cur_date,mode='w')
            f_line = len(exec_file)
            for n in xrange(len(exec_file)):
                if n == f_line-1:
                    sftp_file.write(exec_file[n][0:-1])
                else:
                    sftp_file.write(exec_file[n][0:-1]+'&&')
            sftp.close()
        sclient.close()
