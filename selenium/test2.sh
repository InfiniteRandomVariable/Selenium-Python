#!/bin/bash

BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium"
HUB="javaTest"
NODE="javaNodeTest"
SEL="pythonFront"

INIT_HUB="sh $BASE/$HUB.sh start"
INIT_NODE="sh $BASE/$NODE.sh start"
INIT_SEL="sh $BASE/$SEL.sh start"

STOP_HUB="sh $BASE/$HUB.sh stop"
STOP_NODE="sh $BASE/$NODE.sh stop"
STOP_SEL="sh $BASE/$SEL.sh stop"


PYTHON="python"
PYTHON_FILE="$BASE/$PYTHON.pid"


 case $1 in
    start)
      # echo $! > $PID_FILE;
      #  exec 2>&1 $INIT_HUB 1>/tmp/$HUB.out &
	# wait; exec 2>&1 $INIT_NODE 1>/tmp/$NODE.out &
#	wait; exec 2>&1 $INIT_SEL 1>/tmp/$SEL.out ;;
	$INIT_HUB &
	sleep 5  
	$INIT_NODE &
	sleep 5 
	$INIT_SEL &
	sleep 5 
	wait ;;
	#wait `cat $PYTHON_FILE`
	#echo "ABOUT TO STOP NODE"
	#$STOP_NODE &
	#echo "ABOUT TO STOP HUB"
	#$STOP_HUB & ;; 
	#$INIT_SEL ;;
     stop)
#        exec 2>&1 $STOP_HUB 1>>/tmp/$HUB.out &
#        wait; exec 2>&1 $STOP_NODE 1>>/tmp/$NODE.out &
#        wait; exec 2>&1 $STOP_SEL 1>>/tmp/$SEL.out & ;;

        $STOP_HUB &
        $STOP_NODE &
        $STOP_SEL &
	wait ;;

     *)
        echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0

