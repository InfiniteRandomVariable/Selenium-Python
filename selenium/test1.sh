#!/bin/bash

NAME="notification"
LOG_FILE="/tmp/$NAME.log"
PID_FILE="/var/run/$NAME.pid"
CMD="php /var/www/test/test.php"

function startnotification {
	VAR=`ps -ef | grep "$CMD" | grep -v grep | wc -l`
	if [ $VAR -gt 0 ]; then
		echo "$NAME already running..."
	else
		nohup $CMD > $LOG_FILE 2>&1 &
		echo $! > $PID_FILE
		echo "$NAME listener is started..."
	fi
}

function stopnotification {
	kill `cat /var/run/$NAME.pid`
	rm -f $PID_FILE
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
