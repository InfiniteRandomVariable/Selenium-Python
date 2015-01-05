#!/bin/sh
exec ./wait1.sh 1 >> wait.txt 
./wait2.sh >> wait.txt 
./wait1.sh 3 >> wait.txt
#	./wait2.sh  >> wait.txt
#	 ./wait1.sh 3  >> wait.txt

