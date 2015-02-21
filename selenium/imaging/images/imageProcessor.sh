#!/bin/bash

#/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images


#BASE="./imaging/images"

echo "number of args: $#"
USER_PATH='/usr/local/bin/'

if ( [ "$#" -eq 1 ] ) ; then
	BASE=$1
else
	BASE='/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images'
fi


for img in `ls $BASE`
do

	#per unit 38.75
	defaultWidth=465
	defaultHeight=300
	#defaultWidth=620
	#defaultHeight=420

  	if [ "$img" != "$BASE/imageProcessor.sh" ] ; then

  		##convert lab.tif -resize 50% resize.jpg
  		echo
  		echo
  		echo "START $img"
  		# imagePath="$BASE/$img"
  		imagePath="$BASE"'/'"$img"
  		echo 'START imagePath '"$imagePath"
  		#magickCommand='convert '"$BASE/$img"
		#theType=`identify -format "%m %wx%h" $BASE/$img`

  		magickCommand="$USER_PATH"'convert '"$imagePath"
  		# http://stackoverflow.com/questions/4651437/how-to-set-a-bash-variable-equal-to-the-output-from-a-command
  		theType="$("$USER_PATH"identify -format '%m %wx%h' "$imagePath")"
  		

		#theTypeCommand=(identify -format "%m %wx%h" "$imagePath")
		#echo 'theTypeCommand: '"$theTypeCommand"
		#_theType="${theTypeCommand[@]}"
		#theType=$_theType
		echo "identify1: $theType"
		echo "identify2: ${theType}"
#http://stackoverflow.com/questions/11079342/execute-command-containing-quotes-from-shell-variable

		fileNameJPG=""
		NO='NO'
		YES='YES'
		error=''
		#error='CHANGE LATER'

		##echo $a | tr '[:upper:]' '[:lower:]'
		didUpload=`[[ $img =~ ^.*(uploaded) ]] && echo ${BASH_REMATCH[1]}`

		if [ -z "$didUpload" ] ; then
			imageExtension=`[[ $img =~ ^.*\.(jpg|JPG|JPEG|jpeg|png|PNG|gif|GIF|tiff|TIFF|bmp|BMP)$ ]] && echo ${BASH_REMATCH[1]}`
		else
			error='WARNING: didUpload'
		fi

		

		shouldDelete="$NO"

		echo 'imageExtension: '"$imageExtension"
		 
		if [ ${#imageExtension} -eq 0 ] ; then
			fileNameJPG="$img.jpg"
			shouldDelete="$YES"
		else
			stringToReplace=jpg
	  		fileNameJPG="${img/$imageExtension/$stringToReplace}"
		fi

		if [ "$shouldDelete" == "$NO" ] && [ "$imageExtension" != 'jpg' ] ; then
			shouldDelete="$YES"
		fi 



	  	imageWidth=`[[ $theType =~  [0-9]+ ]] && echo ${BASH_REMATCH[0]}`
	  	imageHeight=`[[ $theType =~  [0-9]+$ ]] && echo ${BASH_REMATCH[0]}`
	  	echo "imageWidth: $imageWidth imageHeight: $imageHeight"

	  	

	  	if [ -z "$imageHeight" ] || [ -z "$imageWidth" ] ; then
	  		error="error imageWidth: $imageWidth imageHeight: $imageHeight"

	  	fi 

	  	if [ "$imageWidth" -lt 150 ] && [ "$imageHeight" -lt 150 ] ; then

	  		error="too small imageWidth: $imageWidth imageHeight: $imageHeight"

	  	elif [ -z "$error" ] && [ "$imageWidth" -lt 300 ] && [ "$imageHeight" -lt 300 ] ; then
			## "Landscape"
			magickCommand=$magickCommand' -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$BASE/$fileNameJPG"

		elif [ -z "$error" ] && [  "$imageWidth" -eq "$imageHeight" ] && [ "$imageWidth" -ge 300 ] ; then
			##"Square"
			magickCommand=$magickCommand' -resize '"$defaultWidth"'x -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$BASE/$fileNameJPG"

		elif [ -z "$error" ] && [ "$imageWidth" -ge "$imageHeight" ] ; then
			## "Landscape"
			magickCommand=$magickCommand' -resize '"$defaultWidth"'x -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$BASE/$fileNameJPG"

		elif [ -z "$error" ] && [ "$imageHeight" -ge "$imageWidth" ] ; then
			## "Portrait"
			magickCommand=$magickCommand' -resize x'"$defaultHeight"' -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$BASE/$fileNameJPG"
		elif [ -z "$error" ] ; then 
			## "error"
			error='minor error: fail to match dimension'
		fi


		#echo "PROCESSING: $magickCommand"

		if [ -z "$error" ] ; then
			echo 'PROCESSING: '"$magickCommand"
			$magickCommand
		fi

		pyExtension=`[[ $img =~ ^.*\.(py|PY|pY|Py|sh|SH|Sh|sH)$ ]] && echo ${BASH_REMATCH[1]}`

		if [ -z "$error" ] && [ "$shouldDelete" == "$YES" ] && [ ${#pyExtension} -eq 0 ]; then
			echo "DELETE: $img"
			rm $imagePath
		fi

		echo $error


	  	##exec $magickCommand

	fi 
 
  #convert $img -filter bessel -resize 30% processed-$img
done

