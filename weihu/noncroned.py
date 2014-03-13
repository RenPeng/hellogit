#!/usr/bin/env python
# -*- coding=utf-8 -*-

import re
import config

def print_nonexec_crontab():
    with  open('/etc/crontab','r') as f:
        lines = f.readlines()
    cur_timelist = config.time_config['cur_min'].split('-')
    
    cur_month = int(cur_timelist[1])
    cur_day = int(cur_timelist[2])
    cur_hour = int(cur_timelist[3])
    cur_minute = int(cur_timelist[4])
    
    for line in lines:
        cron_list = line.split()
        if len(cron_list) < 5:
            pass
        else:
            cron_month = cron_list[3]
            cron_day = cron_list[2]
            cron_hour = cron_list[1]
            cron_minute = cron_list[0]
            cron_name = cron_list[5:]
    
