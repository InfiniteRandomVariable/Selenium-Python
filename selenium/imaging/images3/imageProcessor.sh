#!/bin/sh

#/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images
for img in `ls *`
do

	defaultWidth=620
	defaultHeight=420

  	if [ "$img" != "imageProcessor.sh" ] ; then

  		##convert lab.tif -resize 50% resize.jpg
  		magickCommand='convert '"$img"
		theType=`identify -format "%m %wx%h" $img`
		echo $theType
		
		##echo $a | tr '[:upper:]' '[:lower:]'
		imageExtension=`[[ $img =~ ^.*\.(jpg|JPG|JPEG|jpeg|png|PNG|gif|GIF|tiff|TIFF|bmp|BMP)$ ]] && echo ${BASH_REMATCH[1]}`
	  	stringToReplace=jpg
	  	fileNameJPG="${img/$imageExtension/$stringToReplace}"

	  	imageWidth=`[[ $theType =~  [0-9]+ ]] && echo ${BASH_REMATCH[0]}`
	  	imageHeight=`[[ $theType =~  [0-9]+$ ]] && echo ${BASH_REMATCH[0]}`

	  	error=''

		#if [[ "$theType" != "JPEG"* ]] || [[ "$theType" != "JPG"* ]] ; then

	  		#echo "unmatch: $img type: $theType"
	  		#echo "fileNameJPG: $fileNameJPG extension: $imageExtension"
	  		#magickCommand=$magickCommand" $img $fileNameJPG"
	  		#magickCommand=$magickCommand" $img"


	  	#fi



		if [  $imageWidth -eq $imageHeight ] && [ $imageWidth -ge 100 ] ; then
			##"Square"
			magickCommand=$magickCommand' -resize '"$defaultWidth"'x -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$fileNameJPG"

		elif [ $imageWidth -ge $imageHeight ] ; then
			## "Landscape"
			magickCommand=$magickCommand' -resize '"$defaultWidth"'x -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$fileNameJPG"

		elif [ $imageHeight -ge $imageWidth ] ; then
			## "Portrait"
			magickCommand=$magickCommand' -resize x'"$defaultHeight"' -gravity center -background white -extent '"$defaultWidth"'x'"$defaultHeight"' -crop '"$defaultWidth"'x'"$defaultHeight"' '"$fileNameJPG"
		else
			## "error"
			error='minor error: fail to match dimension'
		fi


		#echo "PROCESSING: $magickCommand"

		if [ ${#error} -eq 0 ] ; then
			echo "PROCESSING: $magickCommand"
			$magickCommand
		fi 

	  	##exec $magickCommand

	fi 
 
  #convert $img -filter bessel -resize 30% processed-$img
done

