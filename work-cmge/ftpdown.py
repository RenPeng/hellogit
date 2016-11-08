#!/usr/bin/env python
# -*- coding=utf-8 -*-
import ftplib

filename = 'patchinfo_rtm.txt'
localfile = '/root/localfile.txt'
file_handler = open(localfile,'wb')
ftp = ftplib.FTP()
ftp.connect(host='118.145.3.88',port=21)
ftp.login(user='patch.hxage.com',passwd='Huruku7uspahEyU4')
ftp.cwd('xytx_rtm')
print ftp.nlst()
ftp.retrbinary("RETR %s" %filename,file_handler.write)
ftp.quit()
file_handler.close()
