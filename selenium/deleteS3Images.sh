#!/bin/bash
BASE="/Users/pro001/Desktop/dev/Learning/tests/scrapWeb/hello-world/selenium"

if ( [ "$#" -eq 1 ] ) ; then
	path=$1
else
	path=$BASE
fi



filePath=$path'/deleteS3Images.py'
python $filePath
