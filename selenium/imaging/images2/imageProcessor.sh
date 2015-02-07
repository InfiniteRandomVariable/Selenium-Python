#!/bin/sh


#NOTE
#the original saved image file format should support common image types
#expect the final image format comply to jpg codec
#/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images

for img in `ls *`
do

	#per unit 38.75
	defaultWidth=465
	defaultHeight=280
	#defaultWidth=620
	#defaultHeight=420

  	if [ "$img" != "imageProcessor.sh" ] ; then

  		##convert lab.tif -resize 50% resize.jpg
  		magickCommand='convert '"$img"
		theType=`identify -format "%m %wx%h" $img`
		echo $theType

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

	  	error=''



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

		if [ -z "$error" ] ; then
			echo 'PROCESSING: '"$magickCommand"
			$magickCommand
		fi


		if [ -z "$error" ] && [ "$shouldDelete" == "$YES" ] ; then
			echo "DELETE: $img"
			rm $img
		fi


	  	##exec $magickCommand

	fi 
 
  #convert $img -filter bessel -resize 30% processed-$img
done

