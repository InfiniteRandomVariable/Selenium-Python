import unittest
import pytz, datetime
import calendar
import re



def timeToTimeStamp(timeStr):
	
	timeZONE = 'US/Eastern'
	##2014-12-20T19:11:26
	
	local = pytz.timezone (timeZONE)
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	#formattedTimeStr = formatString(timeStr)
	#Dec. 14, 2014 13:12  ET
	naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	#print timeStamp
	return timeStamp