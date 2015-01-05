#!/bin/bash

BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium"
HUB="hub"
NODE="node"
SEL=""

INIT_HUB="sh $BASE/$HUB.sh start"
INIT_NODE="sh $BASE/$NODE.sh start"
INIT_SEL="sh $BASE/$SEL.sh start"

STOP_HUB="sh $BASE/$HUB.sh stop"
STOP_NODE="sh $BASE/$NODE.sh stop"
STOP_SEL="sh $BASE/$SEL.sh stop"


 case $1 in
    trial)
	SEL=$2
	echo "TRAIL: $SEL" ;;
    start)
	$INIT_HUB
	sleep 5  
	$INIT_NODE
	sleep 5 
	$INIT_SEL
	wait ;; 
     stop)
        $STOP_HUB 
        $STOP_NODE
        $STOP_SEL ;;

     *)
        echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0

