now=$(date +"%T")
file=~/logs/thirdScript.txt
lines=5
echo "First script current time : $now" >> $file 
tail -n $lines $file > $file.temp
mv $file.temp $file   
