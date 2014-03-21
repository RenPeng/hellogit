#!/bin/sh
if [ ! -d ./log ];then
	mkdir ./log
fi
while read line;
do
	if [[ "$line" =~ ^#.* ]] || [[ "$line" =~ ^$ ]];then
		:
	else
		dir=`echo $line|awk -F, '{print $1}'`
		days=`echo $line|awk -F, '{print $2}'`
		if [ "$dir" == "/" ] || [ -z "${dir}" ] || [ -z "${days}" ];then
			echo "Wrong config line $line "
		else
			echo ----------Start---------- >> ./log/`date +%Y-%m-%d`_Del.log
			find "${dir}" -mtime +${days} -exec ls -l {} \; >> ./log/`date +%Y-%m-%d`_Del.log
			echo -----------End----------- >> ./log/`date +%Y-%m-%d`_Del.log
		fi
	fi
done < config-del.ini
