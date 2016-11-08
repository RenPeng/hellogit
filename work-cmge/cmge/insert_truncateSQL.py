#!/usr/bin/env python
# -*- coding=utf-8 -*-
#!/usr/bin/env python 
import os,sys
import re 


if len(sys.argv) < 2:
    sys.exit("No input file")

file_name = sys.argv[1]
file_obj = open(file_name)
file_content = file_obj.readlines()
file_obj.close()
pattern = r'(dict_\w+|dict_\w+_\w+|server_config|sys_arg|sys_charge_checkin_reward|sys_peroid_card_shop|user_money)'

outputfile = open(sys.argv[1].replace('sql','with_truncate'),'a')
for line in file_content:
    table_name = re.search(pattern,line).group()
    truncate_sql = 'truncate table %s;' % table_name
    outputfile.write(truncate_sql+'\n')
    outputfile.write(line)

outputfile.close()
