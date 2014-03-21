#!/bin/sh
# touch a file in the current dir & let it execable
if [ -z $1 ] || [ -z $2 ];then
printf "Useage: `basename $0` script-name script_type(sh,pl,py)\n"
exit 1
fi

if [ -f $1 ];then
printf  "Fiel $1 exists,please input another name\n"
exit 2
fi

case $2 in
py)
        touch $1 ;chmod a+x $1;echo "#!/usr/bin/env python" > $1 ;;
pl)
        touch $1 ;chmod a+x $1;echo "#!/usr/bin/env perl" > $1 ;;
sh)
        touch $1 ;chmod a+x $1;echo "#!/bin/sh" > $1 ;;
*)
        printf "Error file type '$2'\n"
esac

