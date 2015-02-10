#!/bin/sh
archive_dir=/tmp
script_dir=/home/admin/script
user=dumpuser
port=8904
mysqldump=/data/software/mysql-5.6.17/bin/mysqldump
mysql=/data/software/mysql-5.6.17/bin/mysql
zip=/usr/bin/zip
cur_date=`/bin/date +%Y%m%d`
cur_date_1=`/bin/date +%Y-%m-%d`
iface=`/bin/netstat -rn | awk '{if ($4=="UG") {print $NF}}'`
local_ip=`/sbin/ifconfig ${iface} | awk -F"[ :]+" '/inet addr/ {print $4}'`
username=`/usr/bin/whoami`

# create backup dir
if [ ! -d ${archive_dir}/${cur_date_1} ];then
	mkdir -p ${archive_dir}/${cur_date_1}
fi
# db_backup
for db in `${mysql} -udumpuser -e "show databases"`;do
	if [[ ${db} =~ (Database|mysql|information_schema|performance_schema) ]];then
		continue
	else
            ${mysqldump} -u${user} -P${port} \
		--events --skip-add-drop-table  --add-locks --single-transaction \
		--databases $db > ${archive_dir}/${cur_date_1}/${local_ip}-${cur_date_1}-${db}.sql 
	fi
done

# compress 
cd ${archive_dir}/${cur_date_1}
${zip} ${local_ip}-${cur_date_1}_db.zip ${local_ip}-${cur_date_1}-*.sql > /dev/null 2>&1
/bin/rm -f ${local_ip}-${cur_date_1}-*.sql

if [ $? -eq 0 ];then
	/bin/touch ${archive_dir}/${cur_date_1}/${cur_date_1}.finish
	echo "Compress done!"
fi

# cp zip file to 189 over sftp
/usr/bin/python ${script_dir}/file_upload.py -l ${archive_dir}/${cur_date_1}/${local_ip}-${cur_date_1}_db.zip -r /data/db_backup/${local_ip}/${cur_date_1}
/usr/bin/python ${script_dir}/file_upload.py -l ${archive_dir}/${cur_date_1}/${cur_date_1}.finish -r /data/db_backup/${local_ip}/${cur_date_1}

if [ $? -eq 0 ];then
	echo "Copy file --> backup server  done!"
fi

# clean files older than 5 days
find  ${archive_dir} -mtime +5 -user ${username} -exec rm -rf {} \;
