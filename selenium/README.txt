##imaging
http://stackoverflow.com/questions/11720817/imagemagick-crop-command-not-giving-perfect-result/11721339#11721339
http://stackoverflow.com/questions/8517304/what-the-difference-of-sample-resample-scale-resize-adaptive-resize-thumbnail-im

default size to be 620px width x 465px height

portrait
-resize the image and add blackground
convert images/WPTgp.jpg -resize 290x310 -gravity center -background black -extent 290x310 images/padded.jpg




identify image size
http://stackoverflow.com/questions/1555509/can-imagemagick-return-the-image-size
identify -format "%[fx:w]x%[fx:h]" WPTgp.jpg


#FORMATING IMAGES
First priority
The pixel of the image must not exceeded the specified width. Resize to smaller if needed.

Second priorty
Crop the image the exceed the specified height in equal proportion between bottom and top.

1 step
Is JPG?
	Change to jpg

2 step
What is the pixel dimension?


Square (relative to the width)
	Smaller (not process if 25% smaller)
		resize to fit the width
		S
		same as landscape
	Bigger
		F
		S
		same as landscape
	Match
		S
		same as landscape		

Landscape
	Smaller (not process if 25% smaller)
		nothing
		resize to default width
		add a white background		
	Bigger
		F
		S
		resize to default width
		add a white background		
	Match
		S if applicable
		resize to default width
		add a white background

Portrait
	Smaller (not process if 25% smaller)
		S
		resize to default height
		add a white background
	Bigger
		F
		S
		resize to default height
		add a white background		
	Match
		S
		resize to default height
		add a white background

##commands
	identify size
		size=`identify -format "%[fx:w]x%[fx:h]" padded.jpg`

IMPORTANT:
change the user path for the imageMagick in the imageProcessor.sh file
USER_PATH='/usr/local/bin/'


NOTE:
http://www.fmwconcepts.com/imagemagick/accentedges/index.php

ISSUES:
- deamon can't format and upload the image files to the S3.
	create the output to a designated log file
	possible error - file permission

- nydailynews


Tips: Check if a program exist
http://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script

Atlantic
new format 
.jump-to-comments>a	
