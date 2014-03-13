#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,sys,time

script_dir  = os.path.dirname(__file__)

server_map = {'1\xe8\xa5\xbf\xe6\xb8\xb8\xe5\xa4\xa9\xe4\xb8\x8b':'xytx',
        '2\xe8\xa5\xbf\xe6\xb8\xb8\xe7\xbe\xa4\xe8\x8b\xb1\xe4\xbc\xa0':'xyqyz',
        '4\xe5\xb9\xbb\xe7\x81\xb5\xe4\xbb\x99\xe5\xa2\x83':'hlxj',
        '5\xe9\xac\xaa\xe7\xa5\x9e':'ds'
        } 

dir_config = {'conf_dir':script_dir+'/conf/',
        'execfile_log_dir':script_dir+'/update_log/',
        'result_log_dir':script_dir+'/result_log/',
        'mount_point':'/gamever_down'
        }
conf_config  = {'conf_iplist':dir_config.get('conf_dir')+'iplist.ini',
        'conf_patchinfo':dir_config.get('conf_dir')+'patchinfo.ini',
        'conf_upload':dir_config.get('conf_dir')+'upload_patch.ini',
        }

time_config = {'cur_date':time.strftime('%Y-%m-%d-%H'),
        'cur_mon':time.strftime('%Y-%m'),
        'cur_min':time.strftime('%Y-%m-%d-%H-%M')
        }
'''
logfile ={'exec_file':script_dir+dir_config.get('execfile_log_dir')+\
        sys.argv[1]+'/'+time_config.get('cur_mon')+'/'+time_config.get('cur_date')+'.txt',
        'result_file':script_dir+dir_config.get('result_log_dir')+\
        sys.argv[1]+'/'+time_config.get('cur_mon')+'/'+time_config.get('cur_date')+'.txt'
        }
        '''
