echo "#############################Atlantic about to begin the processes ################"
#echo "process $$"
BASE="/Users/pro001/Desktop/dev/Learning/tests/scrapWeb/hello-world/selenium"
BASE_COMMAND="$BASE/test2.sh"
BASE_IMAGE_COMMAND="$BASE/imaging/images/imageProcessor.sh"

##http://www.politico.com/

#-sh $BASE_COMMAND start atlantic
echo "############################TechCrunch START NEXT PROCESS 1##############################"
#-sh $BASE_COMMAND start techCrunch
echo "############################Wired START NEXT PROCESS 2##############################"
#-sh $BASE_COMMAND start wired
echo "############################WSJ START NEXT PROCESS 3##############################"
#-sh $BASE_COMMAND start wsj
echo "############################youTube START NEXT PROCESS 4##############################"
#-sh $BASE_COMMAND start youTube
echo "############################RottenTomatoes START NEXT PROCESS 5##############################"
#-sh $BASE_COMMAND start rottenTomatoes
echo "############################nyTimes START NEXT PROCESS 6##############################"
#-sh $BASE_COMMAND start nyTimes
echo "############################nyDailyNews START NEXT PROCESS 7##############################"
#-sh $BASE_COMMAND start nyDailyNews
echo "############################Hulu START NEXT PROCESS 8##############################"
#sh $BASE_COMMAND start hulu
echo "############################Guardian START NEXT PROCESS 9##############################"
#-sh $BASE_COMMAND start guardian
echo "############################Bloomberg START NEXT PROCESS 10##############################"
###sh $BASE_COMMAND start bloomberg
echo "############################Billboard START NEXT PROCESS 11##############################"
#-sh $BASE_COMMAND start billboard
echo "############################AmazonBooks START NEXT PROCESS 12##############################"
#sh $BASE_COMMAND start amazonBooks
echo "############################People START NEXT PROCESS 13##############################"
sh $BASE_COMMAND start people
echo "############################IMAGING PROCESS##############################"
sh $BASE_IMAGE_COMMAND
#sh $BASE_COMMAND start people

# echo "############################START NEXT PROCESS 14##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 15##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 16##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 17##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 18##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 19##############################"
# sh test2.sh start
# echo "############################START NEXT PROCESS 20##############################"
# sh test2.sh start

#b=$$
#wait $b
#echo "############################START NEXT PROCESS##############################"
#sh test2.sh start
#b=$!
#wait $b

#sh test2.sh start 
#wait $$ 
#echo "############################START NEXT PROCESS##############################"
#sh test2.sh start
#echo "############################START NEXT PROCESS##############################"
#sh test2.sh start
