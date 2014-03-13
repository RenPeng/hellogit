#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,sys,ConfigParser
import config

#iplist_ini = script_dir+'conf/iplist.ini'  # ip信息列表

class upload_patch(object):
    def __init__(self,absdir):
        self.ftpput = r'/usr/local/bin/ncftpput'
        temp_list = absdir.split('/')
        try:
            with open(self.ftpput) as f:
                pass
        except:
            raise IOError('找不到 ncftpput')
        for l in temp_list:
            if config.server_map.get(l):
                cfp = ConfigParser.ConfigParser()
                cfp.readfp(open(config.conf_config.get('conf_upload')))
                self.server_host = cfp.get(l,'server_patch_host')
                self.client_host = cfp.get(l,'client_patch_host')
                self.server_user = cfp.get(l,'server_patch_user')
                self.client_user = cfp.get(l,'client_patch_user')
                self.server_pass = cfp.get(l,'server_patch_pass')
                self.client_pass = cfp.get(l,'client_patch_pass')
                self.upload(l,absdir)

    def upload(self,server,absdir):
        # 用系统命令上传更新包
        os.system("%s -u %s -p %s %s %s %s%s" \
                %(self.ftpput,self.server_user,self.server_pass,self.server_host,\
                '/ServerPatch',absdir,'/服务器端更新包/*'))
        if config.server_map.get(server) != 'ds':
            os.system("%s -u %s -p %s %s /%s%s %s%s" \
                    %(self.ftpput,self.client_user,self.client_pass,self.client_host,\
                    config.server_map.get(server),'/patch',absdir,'/自动更新包/*'))
            os.system("%s -u %s -p %s %s /%s%s %s%s" \
                    %(self.ftpput,self.client_user,self.client_pass,self.client_host,\
                    config.server_map.get(server),'/down_patch',absdir,'/手动更新包/*'))
        else:
            os.system("%s -u %s -p %s %s /%s%s %s%s" \
                    %(self.ftpput,self.client_user,self.client_pass,self.client_host,\
                    config.server_map.get(server),'_patch',absdir,'/自动更新包/*'))

# 直接调用脚本,调试用
if __name__ == '__main__':
    upload_patch(os.path.dirname(sys.argv[1]))
