import pytz, datetime
import calendar
import re

def formatDisqusString(timeStr):
	#Disqus
	##2014-12-18T13:10:25-05:00
	return re.sub(r'[-|+]\d+:\d+\S$', "",timeStr)

def timeToTimeStamp(timeStr):
	##2014-11-22T16:23:15-0500
	##The 2nd part (-0500) is actually showing what time zone you are in. That means that you are 5 hours behind Greenwich Mean Time (also known as UTC). 
	##-0500 right now is US Central Time. 
	
	local = pytz.timezone ("US/Eastern")
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	formattedTimeStr = formatDisqusString(timeStr)
	naive = datetime.datetime.strptime (formattedTimeStr, "%Y-%m-%dT%H:%M:%S")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	print timeStamp
	return timeStamp

