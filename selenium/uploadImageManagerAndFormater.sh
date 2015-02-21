#!/bin/bash
#echo "process $$"
BASE="/Users/pro001/Desktop/dev/Learning/tests/scrapWeb/hello-world/selenium"
BASE_IMAGE_PATH="$BASE/imaging/images"
BASE_IMAGE_COMMAND="$BASE_IMAGE_PATH/imageProcessor.sh"
BASE_IMAGE_MANAGER="$BASE/uploadImageManager.sh"
BASE_IMAGE_LOG="$BASE_IMAGE_PATH/logs/$(date).log"

echo "############################IMAGE PROCESS ##############################"
##http://www.politico.com/
sh $BASE_IMAGE_COMMAND $BASE_IMAGE_PATH > "$BASE_IMAGE_LOG"
echo "############################PYTHON PROCESS ##############################"
sh $BASE_IMAGE_MANAGER $BASE >> "$BASE_IMAGE_LOG"

