#!/bin/bash


echo "number of args: $#"

START='start'
STOP='stop'

if ( [ "$#" -eq 2 ] && [ "$1" == "$START" ] ) ||  ( [ "$#" -eq 1 ] && [ "$1" == "$STOP" ] ) ; then
	echo "pass"	
else
	echo "require two arguments {start|stop} and publication name"
	exit 0
fi

BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium"
HUB="javaTest"
NODE="javaNodeTest"
SEL=$2

INIT_HUB="sh $BASE/$HUB.sh $START"
INIT_NODE="sh $BASE/$NODE.sh $START"
INIT_SEL="sh $BASE/launchManager.sh $START $SEL"

STOP_HUB="sh $BASE/$HUB.sh $STOP"
STOP_NODE="sh $BASE/$NODE.sh $STOP"
STOP_SEL="sh $BASE/$SEL.sh $STOP"


#PYTHON="python"
#PYTHON_FILE="$BASE/$PYTHON.pid"


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

