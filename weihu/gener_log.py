#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys,os,re,ConfigParser

class gener_log(object):
    def down_patchinfo(self,gp):
        import ftplib
        gp.get_patchinfo()
        if gp.use_ssl == 'no':
            ftp = ftplib.FTP()
        else:
            ftp = ftplib.FTP_TLS()
        for addr in gp.addr_patch.split(','):
            ftp.connect(host=addr,port=gp.port_patch)
            ftp.login(user=gp.user_patch,passwd=gp.pass_patch)
            ftp.cwd(gp.remote_path)
            file_name = os.path.basename(gp.local_file)
            file_dir = os.path.dirname(gp.local_file)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_handler = open(gp.local_file,'w')
            ftp.retrbinary('RETR %s' %file_name,file_handler.write)
            ftp.quit()
            file_handler.close()
    def modif_patchinfo(self,gp):
        '''
        修改patchinfo文件
        '''
        self.down_patchinfo(gp)
        gp.get_patchinfo()
        patchinfo_ini = gp.local_file
        with open(patchinfo_ini) as f:
            lines = f.readlines()
        for n in range(lines.count('\r\n')):
            lines.remove('\r\n')
        for n in range(lines.count('\n')):
            lines.remove('\n')
        for i in xrange(len(lines)):
            if lines[i][-2] == '\r':
                lines[i] = lines[i].replace('\r','')
            if lines[i][-1] == '\r':
                lines[i] = lines[i].replace('\r','\n')
            if lines[i][-1] != '\n':
                lines[i] = lines[i] + '\n'
        if self.autopatch != '' and self.autopatch != lines[3][0:-1].split('/')[-1]:
            aplist = self.autopatch.split('.')
            aplist.remove('zip')
            aplist.remove('autopatch')
            ap_version = '.'.join(aplist)
            ap_url = os.path.dirname(lines[3].split('=')[1][0:-1])+'/'
            lines[2] = '%s%s%s' %('autopatch=',ap_version,'\n')
            lines[3] = '%s%s%s%s' %('newautopatch=',ap_url,self.autopatch,'\n')
            '''
            print '根据配置文件,patchinfo改动如下:'
            print '%s%s\n' %('autopatch=',ap_version),
            print '%s%s%s\n' %('newautopatch=',ap_url,self.autopatch)
            '''
        if self.to_ != '' and self.from_ != '' and self.to_ != lines[1][0:-1].split('=')[1]:
            last_num = int(lines[-4][0:-1].split('_')[1].replace(']','')) + 1
            last_url = os.path.dirname(lines[-1].split('=')[1][0:-1])+'/'
            lines[1] = '%s%s\n' %('latest=',self.to_)
            lines.append('%s%d%s' %('[patch_',last_num,']\n'))
            lines.append('%s%s%s' %('from=',self.from_,'\n'))
            lines.append('%s%s%s' %('to=',self.to_,'\n'))
            lines.append('%s%s%s%s' %('url=',last_url,self.patch,'\n'))
            '''
            print '根据配置文件,patchinfo改动如下:'
            print '%s%s\n' %('latest=',self.to_),
            print '%s%d%s\n' %('[patch_',last_num,']'),
            print '%s%s\n' %('from=',self.from_),
            print '%s%s\n' %('to=',self.to_),
            print '%s%s%s\n' %('url=',last_url,self.patch),
            '''
        with open(patchinfo_ini,'w') as f:
            f.writelines(lines)
        if self.to_ != '' or self.from_ != ''or self.autopatch != '':
            return 'yes'
    def GetServerUpdateList(self,mode,update_desc):
        ''' 
        统计更新说明中有多少个服务器更新包,并存放到ser_patch_dict字典中
        '''
        cfp = ConfigParser.ConfigParser()
        cfp.readfp(open(update_desc))
        if mode.split('-')[1] == 'rtm':
            server = '正式服'.decode('utf-8').encode('gbk')
        elif mode.split('-')[1] == 'beta':
            server = '体验服'.decode('utf-8').encode('gbk')
        else:
            sys.exit('在更新说明中找不到与%s对应的配置',mode.split('-')[1])
        option_list = cfp.options(server)
        update_list = []
        self.ser_patch_dict = {}
        # 获取更新包列表
        for i in option_list:
            if re.findall('服务器端更新包'.decode('utf-8').encode('gbk'),i):
                update_list.append(i)
        # 更新包字典
        update_list.sort()
        for n in xrange(len(update_list)):
            self.ser_patch_dict[n] = cfp.get(server,'服务器端更新包'.decode('utf-8').encode('gbk')+str(n+1))
        self.from_ = cfp.get(server,'from')
        self.to_ = cfp.get(server,'to')
        self.autopatch = cfp.get(server,'autopatch')
        self.update_time = cfp.get(server,'更新时间'.decode('utf-8').encode('gbk'))
        self.patch = cfp.get(server,'自动更新包'.decode('utf-8').encode('gbk'))
        self.manual_patch = cfp.get(server,'手动更新包'.decode('utf-8').encode('gbk'))
    def GenerUpdateFile(self,mode,update_file):
        '''
        生成更新日志
        '''
        file_handler = open(update_file,'w')
        if self.ser_patch_dict[0] != '':
            for n in xrange(len(self.ser_patch_dict)):
                file_handler.write('%s%s\n' %('cd && wget -c http://lab.hxage.net/ServerPatch/',self.ser_patch_dict[n]))
                file_handler.write('%s%s%s%s\n' %('unzip -o -d /data/',mode.split('-')[0],\
                        'GameServer /home/gm/',self.ser_patch_dict[n]))
                if mode  == 'ds-beta' or mode == 'xyol-beta':
                    file_handler.write('%s%s%s%s\n' %('unzip -o -d /data/',mode.split('-')[0],\
                            'GameServer_time /home/gm/',self.ser_patch_dict[n]))
                    file_handler.write('%s%s%s\n' %('chmod +x /data/',mode.split('-')[0],'GameServer_time/Server/*'))
            file_handler.write('%s%s%s\n' %('chmod +x /data/',mode.split('-')[0],'GameServer/Server/*'))
            file_handler.close()
            return 'yes'

# 测试用
if __name__ == '__main__':
    pass
