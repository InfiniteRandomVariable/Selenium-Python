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

 case $1 in
    start)
      # echo $! > $PID_FILE;
      #  exec 2>&1 $INIT_HUB 1>/tmp/$HUB.out &
	# wait; exec 2>&1 $INIT_NODE 1>/tmp/$NODE.out &
#	wait; exec 2>&1 $INIT_SEL 1>/tmp/$SEL.out ;;
#echo 'command1 --foo=bar' | batch
#echo 'command2' | batch
#at -q b -l              # on many OSes, a slightly shorter synonym is: atq -q b
	$INIT_HUB | batch &
	$INIT_NODE | batch &
	$INIT_SEL | batch & ;;
     stop)
        exec 2>&1 $STOP_HUB 1>>/tmp/$HUB.out &
        wait; exec 2>&1 $STOP_NODE 1>>/tmp/$NODE.out &
        wait; exec 2>&1 $STOP_SEL 1>>/tmp/$SEL.out & ;;
     *)
        echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0

