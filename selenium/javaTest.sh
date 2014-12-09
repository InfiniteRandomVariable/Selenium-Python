#!/bin/bash

NAME="selenium_hub"
LOG_FILE="/tmp/$NAME.log"
BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb"
PID_FILE="$BASE/hello-world/selenium/$NAME.pid"
SEL_SERVER="$BASE/selenium-server-standalone-2.44.0.jar"
CONFIG="$BASE/hello-world/selenium/hubConfig.json"

INIT_HUB="java -jar $SEL_SERVER -role hub -hubConfig $CONFIG"



 case $1 in
    start)
      # echo $! > $PID_FILE;
	exec 2>&1 $INIT_HUB 1>/tmp/$NAME.out &
	PID=$!
	echo $PID > $PID_FILE;;
     stop)
	# try to kill process, if succeed, remove the file else kill the process by jps 
	kill `cat $PID_FILE` && rm -f $PID_FILE || jps -l | grep $SEL_SERVER | cut -d ' ' -f 1 | xargs -n1 kill;; 
     *)  
	echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0