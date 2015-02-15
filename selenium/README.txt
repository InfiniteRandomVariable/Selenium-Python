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



NOTE:
http://www.fmwconcepts.com/imagemagick/accentedges/index.php

ISSUES:
- deamon can't format and upload the image files to the S3.
	create the output to a designated log file
	possible error - file permission

- nytimes
- atlantic
- nydailynews
- WSJ

			bogon:selenium pro001$ python wsj.py
			Total Articles: 2
			numComments 30 
			timeStr Feb. 13, 2015 7:32 p.m. ET
			article.age 1423873920 
			container
			article.topComment The GD were the WORST band of their era. Their fans...what can I say....So many good bands started then. I enjoy them to this day. Living with Dead heads in my college dormitories was a frightening and depressing thing. I never want to hear their "music" again.  
			about to call getImageAndSave
			0 imageProcedure
			1 imageProcedure
			imageURLFormatter
			imageTitle: -Ends-in name: ----18-4M.jpguploaded
			imageTitle: -Ends-in name: ----23-3M.jpguploaded
			imageTitle: -Ends-in name: ----55-4M.jpguploaded
			imageTitle: -Ends-in name: --2-11-15.jpguploaded
			imageTitle: -Ends-in name: --comment.jpguploaded
			imageTitle: -Ends-in name: --Ep--14.jpguploaded
			imageTitle: -Ends-in name: --Triumph.jpguploaded
			imageTitle: -Ends-in name: -air-base.jpguploaded
			imageTitle: -Ends-in name: -Al-Qaeda.jpguploaded
			imageTitle: -Ends-in name: -Bentley.jpguploaded
			imageTitle: -Ends-in name: -Building.jpguploaded
			imageTitle: -Ends-in name: -Business.jpguploaded
			imageTitle: -Ends-in name: -cover-up.jpguploaded
			imageTitle: -Ends-in name: -Ends-in.jpguploaded
			MATCH imageTitle: -Ends-in name: -Ends-in.jpguploaded
			return from getImageAndSave True
			imageURLFormatter
			urlTitle: -Ends-in
			final URLTitle: i/-Ends-in.jpg
			failed url: http://www.wsj.com/articles/for-grateful-deads-final-shows-long-strange-trip-ends-in-sea-of-mail-1423873970?mod=trending_now_3
			Exception: 'ascii' codec can't encode character u'\u2019' in position 17: ordinal not in range(128)
			numComments 69 
			timeStr Updated Feb. 13, 2015 6:57 p.m. ET
			article.age 1423871820 
			container
			article.topComment What does this have to do with Wall Street? I don't subscribe to read about dogmatic religions and opinions about them 
			about to call getImageAndSave
			0 imageProcedure
			1 imageProcedure
			imageURLFormatter
			imageTitle: Arab-Jews name: ----18-4M.jpguploaded
			imageTitle: Arab-Jews name: ----23-3M.jpguploaded
			imageTitle: Arab-Jews name: ----55-4M.jpguploaded
			imageTitle: Arab-Jews name: --2-11-15.jpguploaded
			imageTitle: Arab-Jews name: --comment.jpguploaded
			imageTitle: Arab-Jews name: --Ep--14.jpguploaded
			imageTitle: Arab-Jews name: --Triumph.jpguploaded
			imageTitle: Arab-Jews name: -air-base.jpguploaded
			imageTitle: Arab-Jews name: -Al-Qaeda.jpguploaded
			imageTitle: Arab-Jews name: -Bentley.jpguploaded
			imageTitle: Arab-Jews name: -Building.jpguploaded
			imageTitle: Arab-Jews name: -Business.jpguploaded
			imageTitle: Arab-Jews name: -cover-up.jpguploaded
			imageTitle: Arab-Jews name: -Ends-in.jpguploaded
			imageTitle: Arab-Jews name: -Engineer.jpguploaded
			imageTitle: Arab-Jews name: -Governor.jpguploaded
			imageTitle: Arab-Jews name: -Grenade.jpguploaded
			imageTitle: Arab-Jews name: -Insanity.jpguploaded
			imageTitle: Arab-Jews name: -isis-war.jpguploaded
			imageTitle: Arab-Jews name: -licenses.jpguploaded
			imageTitle: Arab-Jews name: -megastar.jpguploaded
			imageTitle: Arab-Jews name: -Movie-HD.jpguploaded
			imageTitle: Arab-Jews name: -national.jpguploaded
			imageTitle: Arab-Jews name: -of-Cards.jpguploaded
			imageTitle: Arab-Jews name: -on-alert.jpguploaded
			imageTitle: Arab-Jews name: -Payments.jpguploaded
			imageTitle: Arab-Jews name: -revealed.jpguploaded
			imageTitle: Arab-Jews name: -Says-WSJ.jpguploaded
			imageTitle: Arab-Jews name: -SEASON-1.jpguploaded
			imageTitle: Arab-Jews name: -SPECTRE.jpguploaded
			imageTitle: Arab-Jews name: -strategy.jpguploaded
			imageTitle: Arab-Jews name: -Together.jpguploaded
			imageTitle: Arab-Jews name: .DS_Store
			imageTitle: Arab-Jews name: 000-Years.jpguploaded
			imageTitle: Arab-Jews name: a-Johnson.jpguploaded
			imageTitle: Arab-Jews name: Advantage.jpguploaded
			imageTitle: Arab-Jews name: an-Eraser.jpg
			imageTitle: Arab-Jews name: AN-on-TBS.jpguploaded
			imageTitle: Arab-Jews name: an-Reedus.jpguploaded
			imageTitle: Arab-Jews name: ank-space.jpguploaded
			imageTitle: Arab-Jews name: apel-hill.jpguploaded
			imageTitle: Arab-Jews name: Arab-Jews.jpguploaded
			MATCH imageTitle: Arab-Jews name: Arab-Jews.jpguploaded
			return from getImageAndSave True
			imageURLFormatter
			urlTitle: Arab-Jews
			final URLTitle: i/Arab-Jews.jpg
			failed url: http://www.wsj.com/articles/insular-jewish-community-of-djerba-tunisia-has-weathered-revolution-and-terrorism-but-can-it-survive-girls-education-1423869146?mod=trending_now_5
			Title: The Last of the Arab Jews
			URL: http://www.wsj.com/articles/insular-jewish-community-of-djerba-tunisia-has-weathered-revolution-and-terrorism-but-can-it-survive-girls-education-1423869146?mod=trending_now_5
			NumComments: 69
			TopComment: What does this have to do with Wall Street? I don't subscribe to read about dogmatic religions and opinions about them
			TopCommentNum: 0
			Age: 1423871820
			Tag: popular
