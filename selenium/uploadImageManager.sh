#!/bin/bash


if ( [ "$#" -eq 1 ] ) ; then
	echo "pass"
	path=$1
else
	echo "require one arguments for path name to the python script"
	path='/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium'
fi



filePath=$path'/uploadImageManager.py'
python $filePath