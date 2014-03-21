#!/bin/sh
i=\=
for ((d=0;d<=100;d+=2 ));do
		printf "[%-50s]%d%%\r" $i $d
		sleep 0.1
		i=\=$i
done
echo 
