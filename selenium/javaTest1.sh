#!/bin/bash

NAME="selenium_hub"
LOG_FILE="/tmp/$NAME.log"
PID_FILE="/var/run/$NAME.pid"
SEL_SERVER="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/selenium-server-standalone-2.44.0.jar"
CONFIG="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/hubConfig.json"

INIT_HUB="java -jar $SEL_SERVER -role hub -hubConfig $CONFIG"

function startnotification {
	VAR=`ps -ef | grep "$INIT_HUB" | grep -v grep | wc -l`
	if [ $VAR -gt 0 ]; then
		echo "$NAME already running..."
	else
#remove nohup $INIT_HUB > $LOG_FILE 2>&1 &
		nohup $INIT_HUB > $LOG_FILE 2>&1
		sudo -s "echo $! > $PID_FILE"
		cat $PID_FILE
		echo "$NAME listener is started..."
	fi
}

#double safe
#try to use JPS to kill JAVA process
#try to use datafile to kill process

function stopnotification {
	jps -l | grep $SEL_SERVER | cut -d ' ' -f 1 | xargs -n1 kill
	kill `cat /var/run/$NAME.pid`
	sudo -s "rm -f $PID_FILE"
	echo "$NAME listener stopped."
}
case $1 in
	start) startnotification;;
	stop)  stopnotification;;
	restart)
	stopnotification
	startnotification;;
*)
	echo "usage: $NAME {start|stop}" ;;
esac

exit 0
