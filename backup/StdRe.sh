#!/bin/sh
exec 3>&1
exec > number
/bin/ls -l
ls
df
exec 1>&3 3>&-
echo aaa
echo bbb
