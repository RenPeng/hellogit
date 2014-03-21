#!/bin/sh
# 版本信息
# v-1.2		将脚本中的echo修改为printf,增加可移植性
# v-1.3		增加debug功能
# v-1.4.1	配置文件中的文件名称可以使用*等匹配字符
# v-1.4.2	如果命令行参数中没有-s选项，则备份指定的配置文件中所有模块
# v-1.4.3	配置文件中增加[DEL_OLDFILE]选项,用于N天之前的备份文件
# v-1.4.4	将脚本中的管道尽省略
# v-1.4.5	配置文件可以指定多个数据库、目录进行备份,格式如mysql,test_db,名称之间用','隔开(注意不要使用中文逗号)
# v-1.4.6	增加变量检查功能,如果变量为空将放弃该Section的备份;将邮件报警收件人写入全局配置文件
# v-1.4.7	修正删除旧文件不及时;ftp上传目录如果不存在则创建,不会因为上传目录不存在而失败
# v-1.4.8	更换压缩工具为RAR
# v-1.4.9	规范备份目录结构
version=1.4.9


## 脚本状态说明
# 2:脚本参数错误
# 3:备份文件失败
# 4:mysqldump备份失败
# 5:将mysqldump备份的文件打包失败
# 6:变量为空
# 10:需要备份的数据库不存在

# 帮助函数
function help()
{
	printf "Usage: `basename $1` <-g> <-c> <-f> [-s] [-h] [-d]
Option:
-g	:global configfile
-c	:config file name
-s	:Secion name in configfile
-f	:ip address of ftp server
-h	:print useage and exit
-d	:Debug mode(print the error info to STDOUT)

Example: 
`basename $1` -g global.ini -c web.ini -f 192.168.0.106 [-s server_apache] 
"
exit 1
}
# 报警模块
function warning
{
if [ -n "$1" ];then
	cat -
else
	# 判断报错文件时候存在,选择是否attached
	if [ ! -f "${v_errorlog}" ];then
		${scpwd}/mail/mutt -F ${scpwd}/mail/muttrc  -s "Backup Failed [${v_host}-${v_ip}]"  \
		${v_eaddr}
	else
		${scpwd}/mail/mutt -F ${scpwd}/mail/muttrc -a ${v_errorlog} -s "Backup Failed [${v_host}-${v_ip}]"  \
		${v_eaddr}
	fi
fi
}

function chkconf()
{
if [ ! -f $1 ];then
	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
\tError Message: Please check parameter [$1] on the command line,file [$1] not exist.\n" | warning ${debug}
	exit 2
fi
}

# 读取参数中的配置文件名称

if [ $# -lt 6 ];then
		help $0
else
	echo $@ | grep "\-d" >> /dev/null 2>&1
		if [ $? -eq 0 ];then
			debug=debug
		else
			debug=""
		fi
fi

while [ $# -gt 0 ] 
do
	case $1 in
		-g)
   			f_global=$2
			chkconf ${f_global}
   			shift 2;; 
		-c)
  			f_config=$2
			chkconf ${f_config}
   			shift 2;; 
		-s)
   			f_section=$2
   			shift 2;; 
		-f)
   			f_ftpip=$2
   			shift 2;; 
		-d)
			debug=debug
			shift 1;;
		-h|-help)
   			help $0;;
		*)
   			help $0;;
		esac
done

# 解密函数
decrypt ()
{
    [[ -n $1 ]] && epw=`printf "$1\n"|tr "[B-Z]A[b-z]a[2-9]10" "[a-y]z[A-Y]Z[0-7]89"`;
    epw=${epw%`whoami`};
    PW=`printf "${epw}\n"|tr "[B-Z]A[b-z]a[2-9]10" "[a-y]z[A-Y]Z[0-7]89"`
		printf "${PW}\n"
}

# 提取配置文件中相应参数的值
	function v_ip()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/IP=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_switcher()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/SWITCHER=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_type()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/TYPE=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_ftpput()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/FTP_PUT=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}

	function v_ftppath()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/FTP_PATH=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_dbname()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/DATABASE_NAME=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_dirname()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/DIR_NAME=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}

	function v_filename()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/FILE_NAME=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p' | tr -d ' '
	}

	function v_filepath()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/FILE_PATH=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_bakpath()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/BAK_PATH=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_dbuser()
	{ decrypt `sed -ne '/\['$1'\]/,/\[.*\]/ s/DATABASE_USER=//p' ${f_config} | sed -ne 's/^ *//' -ne 's/ *$//p'`
	}
	function v_dbpass()
	{ decrypt `sed -ne '/\['$1'\]/,/\[.*\]/ s/DATABASE_PASS=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p'`
	}
	function v_deloldfile()
	{ sed -ne '/\['$1'\]/,/\[.*\]/ s/DEL_OLDFILE=//p' ${f_config}  | sed -ne 's/^ *//' -ne 's/ *$//p'
	}

# Global 变量提取

	function v_tar()
	{ sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/TAR=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_ftp()
	{ sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/NCFTPPUT=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_mysqlbin()
	{ sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/MYSQL_BIN=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_eaddr()
	{ sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/EADDR=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'
	}
	function v_ftpuser()
	{ decrypt `sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/FTP_USER=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'` 
	}
	function  v_ftppass()
	{ decrypt `sed -ne '/\[PUBLIC\]/,/\[.*\]/ s/FTP_PASS=//p' ${f_global} | sed -ne 's/^ *//' -ne 's/ *$//p'`
	}



# 判断备份是否成功
function bakcheck()
{ if [  $? -eq 0 ];then
	printf "\tbackup [%s] success\n" "$1"
	return 0
else

	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
	\tError Message: Backup [${1}] that configed in [${f_config}]-[${i}] Failed.
	\tYou can get more info from ${v_errorlog}\n"| warning ${debug}

	return 3
fi
}
# 删除旧文件
function deloldfile()
{ if [ "${v_deloldfile}" -ne "0" ];then

	printf "$(date +%F" "%T)\n" >> "${new_bakpath}"/delfile.log

	find "${new_bakpath}"/ -mtime ${v_deloldfile}  -type f | xargs -i rm -rfv {} >> "${new_bakpath}"/delfile.log 2>&1 

	find ${HOME} -name "_backlog-*" | xargs -i rm -rfv {} >> "${new_bakpath}"/delfile.log 2>&1

  else

	printf "\tDelete switcher if off\n"
fi
}
# 检查变量是否为空
function check_var()
{
	if [ "$1" == "null" ];then
		printf "\tVariable [$2] is empty,please check\n"
		break
		return 6
	fi
}

# 备份文件
function bak_file()
{ 
# 创建bakpath
	if [ ! -d ${v_bakpath}/${v_year}/${v_month}/${v_day} ];then
		mkdir -p "${v_bakpath}/${v_year}/${v_month}/${v_day}" > /dev/null 2>&1
	fi
	new_bakpath=${v_bakpath}/${v_year}/${v_month}/${v_day}
	cd ${scpwd}

if [ -n "${v_dbname}" ];then
	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
	\tError Message: Error file TYPE,please check your Section [$i]\n"| warning ${debug}
	return 4
else
	if [ -n "${v_filepath}" ];then
		# 文件开始备份
		printf "[Section:$i-file]\n"
			# 检查变量是否为空
			check_var	${v_filename:=null} FILE_NAME
			check_var	${v_filepath:=null} FILE_PATH
			check_var	${v_ip:=null} IP
			check_var	${v_bakpath:=null} BAK_PATH
			check_var	${v_deloldfile:=null} DEL_OLDFILE
			check_var	${v_ftpput:=null} FTP_PUT
			check_var	${v_ftppath:=null} FTP_PATH
			cd ${v_filepath} > /dev/null 2>&1
			export filelist=$(echo ${v_filename} |tr "," " ")
			deloldfile
			${v_tar} a "${new_bakpath}"/${i}.rar  ${filelist} > ${v_errorlog} 2>&1
			# 判断备份是否成功
					bakcheck ${i}.rar
			cd ${scpwd}
			# 文件备份结束
	else
		# 目录开始备份
		printf "[Section:$i-Dir]\n"
		check_var	${v_dirname:=null} DIR_NAME
		check_var	${v_ip:=null} IP
		check_var	${v_bakpath:=null} BAK_PATH
		check_var	${v_deloldfile:=null} DEL_OLDFILE
		check_var	${v_ftpput:=null} FTP_PUT
		check_var	${v_ftppath:=null} FTP_PATH

		export dirlist=$(echo ${v_dirname} |tr "," " ")
		deloldfile # 删除旧文件
		# 开始备份
			cd ${v_dir_name}
			${v_tar} a  "${new_bakpath}"/${i}.rar  ${dirlist}  > ${v_errorlog} 2>&1
		# 判断备份是否成功
			bakcheck ${i}.rar
			cd ${scpwd}
		#备份不成功返回状态3
			if [ $? -eq 0 ];then
				:
				#cd -  >> /dev/null 2>&1
			else
				return 3
			fi
			#cd - > /dev/null 2>&1
		# 目录结束备份
	fi
fi
}


# 备份数据库
function bak_db()
{ 
if [ -n "${v_dirname}" ] || [ -n "${v_filename}" ];then
	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
	\tError Message: Error file TYPE,please check your Section [$i]\n"| warning ${debug}
	return 4
else
printf "[Section:$i-DB]\n"

# 检查变量是否为空
	check_var	${v_ip:=null} IP
	check_var	${v_dbuser:=null} DATABASE_USER
	check_var	${v_dbpass:=null} DATABASE_PASS
	check_var	${v_dbname:=null} DATABASE_NAME
	check_var	${v_bakpath:=null} BAK_PATH
	check_var	${v_ftpput:=null} FTP_PUT
	check_var	${v_ftppath:=null} FTP_PATH
	check_var	${v_deloldfile:=null} DEL_OLDFILE

# 创建bakpath
	if [ ! -d ${v_bakpath}/${v_year}/${v_month}/${v_day} ];then
		mkdir -p "${v_bakpath}/${v_year}/${v_month}/${v_day}" > /dev/null 2>&1
	fi
	new_bakpath=${v_bakpath}/${v_year}/${v_month}/${v_day}
	deloldfile
	export dblist=$(echo ${v_dbname} |tr "," " ")
	for d in ${dblist};
		do
		# 判断数据库是否存在
		db=`${v_mysqlbin}/bin/mysql -u${v_dbuser} -p${v_dbpass} -e"show databases;" 2>> ${v_errorlog} | grep ${d}`
			if [ -z "$db" ];then
				printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
				\tError Message: DB [${v_dbname}] does not exist or mysql is not available.
				\tDatabase [${v_dbname}] that configed in [${f_config}]-[${i}] couldn't  backup.
				\tYou can get more info from ${v_errorlog}\n"	| warning ${debug}
				return 10
			fi
		done
	#数据库开始备份
			${v_mysqlbin}/bin/mysqldump -u ${v_dbuser} -p${v_dbpass} -R \
			--single-transaction --databases ${dblist} >  "${new_bakpath}"/${i}.sql 2>> ${v_errorlog}
				# 判断备份是否成功
			bakcheck ${i}.sql
			if [ $? -eq 3 ];then
					return 3
			else
				# 将sql文件打包
				cd ${new_bakpath}
				${v_tar} a -HPHp2LZYzw ${i}.rar ${i}.sql  > ${v_errorlog} 2>&1
					if [ $? -eq 0 ];then
						rm -rf "${new_bakpath}"/${i}.sql
					else
						return 3
					fi
		cd ${scpwd} > /dev/null 2>&1
	fi
fi
}


# 检查上传到ftp文件完整性
function uploadcheck()
{ 
ftpsize=`/usr/local/bin/ncftpls  -u ${v_ftpuser} -p ${v_ftppass} -la  \
		ftp://${v_ftpip}/"${v_ftppath}" 2>> ${v_errorlog} | grep $1 |awk '{print $5}'`
localsize=`ls -l "${new_bakpath}"/$1 2>> ${v_errorlog} | awk '{print $5}'`
if [ -z "${localsize}" ];then
		printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
		\tError Message: couldn't find ${v_bakpath}/$1,upload fail.\n"| warning ${debug}
	else if [ -z "${ftpsize}" ];then
		printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
		\tError Message: Can't reach FTP server or 'ncftpls' command not fonud, couldn't get the size of uploaded file\n"| warning ${debug}

	else if [ "${ftpsize}" -eq "${localsize}" ];then

		printf "\tupload $1 success\n"

else

	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
	\tError Message: File [%s] upload Failed\n" "$1" | warning ${debug}

	fi

	fi

fi
}



# 上传到ftp服务器
function upload()
{ if [ "${v_type}" = 0 ];then

	if [ ! -z "${v_filename}" ];then
		${v_ftp}  -u ${v_ftpuser} -p ${v_ftppass} -m ${v_ftpip} "${v_ftppath}" "${new_bakpath}"/${i}.rar 2>> \
	${v_errorlog}

	uploadcheck ${i}.rar

	else
		${v_ftp}  -u ${v_ftpuser} -p ${v_ftppass} -m  ${v_ftpip} "${v_ftppath}" "${new_bakpath}"/${i}.rar 2>> \
	${v_errorlog}

	uploadcheck ${i}.rar

	fi
else 
	${v_ftp}  -u ${v_ftpuser} -p ${v_ftppass} -m ${v_ftpip} "${v_ftppath}" "${new_bakpath}"/${i}.rar 2>> \
	${v_errorlog}

	uploadcheck ${i}.rar

fi
}

function ftpswitch()
{ if [ $? -eq 0 ];then
	if [ "$1" == "0" ];then
		upload
		printf "\n"
	else
		printf "\tFTP_PUT is off\n"
		printf "\n"
	fi
  else
	printf  "\tCommand line: -g ${f_global} -c ${f_config} -f ${f_ftpip}
	\tError Message: Backup failed,can't upload\n" | warning ${debug}
	printf "\n"
	return 3
fi
}

# 判断需要备份的Section
if [ -z "${f_seciton}" ];then
	baklist=`sed -ne '/\[.*\]/ s/\[//;s/\]//p' ${f_config}`
else
	baseparm1=`echo ${f_section} | awk -F- '{print $1}' `
	baseparm2=`echo ${f_section} | awk -F- '{print $2}' `
	if [ -z  "${baseparm2}" ];then 
		baklist=`sed -ne '/\['${baseparm1}'-.*}\] s/\[//;s/\]//p' ${f_config}`
	else
		baklist=`sed -ne '/\['${f_section}'\]/ s/\[//;s/\]//p'`
	fi
fi

# 开始进行备份

for i in $baklist
do
# 全局变量
	v_ip=`v_ip $i`
	v_deloldfile=`v_deloldfile $i`
	v_switcher=`v_switcher $i`
	v_type=`v_type $i`
	v_ftpput=`v_ftpput $i`
	v_ftppath=`v_ftppath $i`
	v_bakpath=`v_bakpath $i`
	v_dbuser=`v_dbuser $i`
	v_dbpass=`v_dbpass $i`
	v_dbname=`v_dbname $i`
	v_filename=`v_filename $i`
	v_filepath=`v_filepath $i`
	v_dirname=`v_dirname $i`

	v_tar=`v_tar`
	v_ftp=`v_ftp`
	v_ftpip=${f_ftpip}
	v_date=`date +%Y-%m-%d`
	v_year=`date +%Y`
	v_month=`date +%m`
	v_day=`date +%d`
	v_hour=`date +%H`
	v_host=`hostname`
	v_errorlog=${v_bakpath}/${v_year}/${v_month}/${v_day}/_backlog-${v_date}.log
	v_mysqlbin=`v_mysqlbin`
	v_ftpuser=`v_ftpuser`
	v_ftppass=`v_ftppass`
	v_eaddr=`v_eaddr`
	scpwd=`/usr/bin/dirname $0`
	echo 1234
	echo $scpwd
	if [ "${v_switcher}" == "0" ];then
		while [ ! -z $i ]
		do
			s=$v_type
		case $s in
			0)
				bak_file;
				ftpswitch ${v_ftpput};
				break;;
			1)
				bak_db;
				ftpswitch ${v_ftpput};
				break;;
			*)
			printf "${f_config}-$i-TYPE ERROR!!!\n"
				break;;
		esac
		done
	else
		printf "[Section:$i]\n"
		printf "\t${f_config}-$i Switcher is off\n"
	fi
done
