#!/bin/bash

NAME="python"
BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb"
PID_FILE="$BASE/hello-world/selenium/$NAME.pid"
SEL_SERVER="$BASE/selenium-server-standalone-2.44.0.jar"
CONFIG="$BASE/hello-world/selenium/hubConfig.json"

LOG_FILE="/tmp/$NAME.log"
#PID_FILE="/var/run/$NAME.pid"
#PYTHON="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/frontAtlantic.py"
PYTHON="$BASE/hello-world/selenium/frontAtlantic.py"

INIT_HUB="python $PYTHON"



 case $1 in
    start)
	pkill firefox-bin
	kill `cat $PID_FILE`
	rm -f $PID_FILE
	exec 2>&1 $INIT_HUB 1>/tmp/$NAME.out &
	PID=$!
	echo $PID
	echo $PID > $PID_FILE;;
     stop)
	pkill firefox-bin
	# try to kill process, if succeed, remove the file else kill the process by jps 
	kill `cat $PID_FILE`
	rm -f $PID_FILE;;
     *)  
	echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0
