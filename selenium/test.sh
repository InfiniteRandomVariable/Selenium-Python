SELENIUM_PROGRAM=/usr/bin/java
SELENIUM_OPTS="-jar  ~/Desktop/Dev/Learning/tests/scrapWeb/selenium-server-standalone-2.44.0.jar -role node  -hub http://localhost:4444/grid/register"
SELENIUM_PID_NAME=selenium
SELENIUM_LOG_FILE=selenium.logfile
sudo -s "$SELENIUM_PROGRAM $SELENIUM_OPTS 2>&1 >>$SELENIUM_LOG_FILE"
PID=$!
echo $PID > $SELENIUM_PID_NAME.pid

