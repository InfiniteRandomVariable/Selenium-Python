#!/bin/sh

#/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images
BASE="./imaging/images"
for img in `ls $BASE`
do

	#per unit 38.75
	defaultWidth=465
	defaultHeight=300
	#defaultWidth=620
	#defaultHeight=420

  	if [ "$img" != "imageProcessor.sh" ] ; then

  		##convert lab.tif -resize 50% resize.jpg
  		echo
  		echo
  		echo "START $img"
  		imagePath="$BASE/$img"
  		#magickCommand='convert '"$BASE/$img"
		#theType=`identify -format "%m %wx%h" $BASE/$img`

  		magickCommand='convert '"$imagePath"
		theType=`identify -format "%m %wx%h" $imagePath`

		echo "identify: $theType"

		fileNameJPG=""
		NO='NO'
		YES='YES'
		
		##echo $a | tr '[:upper:]' '[:lower:]'
		imageExtension=`[[ $img =~ ^.*\.(jpg|JPG|JPEG|jpeg|png|PNG|gif|GIF|tiff|TIFF|bmp|BMP)$ ]] && echo ${BASH_REMATCH[1]}`

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

	  	error=''

	  	if [ -z "$imageHeight" ] || [ -z "$imageWidth" ] ; then
	  		error="error imageWidth: $imageWidth imageHeight: $imageHeight"

	  	fi 

	  	



		if [ -z "$error" ] && [  "$imageWidth" -eq "$imageHeight" ] && [ "$imageWidth" -ge 100 ] ; then
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


	  	##exec $magickCommand

	fi 
 
  #convert $img -filter bessel -resize 30% processed-$img
done

