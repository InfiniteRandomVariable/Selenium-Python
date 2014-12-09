#!/bin/bash

NAME="selenium_node"
LOG_FILE="/tmp/$NAME.log"
PID_FILE="/var/run/$NAME.pid"
SEL_SERVER="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/selenium-server-standalone-2.44.0.jar"
CONFIG="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/hubConfig.json"
HOST="http://localhost:4444/grid/register"

INIT_NODE="java -jar $SEL_SERVER -role node -hub $HOST"

 case $1 in
    start)
      # echo $! > $PID_FILE;
	exec 2>&1 $INIT_NODE 1>/tmp/$NAME.out &
	PID=$!
	sudo -s "echo $PID > $PID_FILE";;
     stop)
	jps -l | grep $SEL_SERVER | cut -d ' ' -f 1 | xargs -n1 kill  
	kill `cat $PID_FILE`
	sudo -s "rm -f $PID_FILE" ;;
     *)  
	echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0
