import pytz, datetime
import calendar
import re

def formatAtlanticString(timeStr):
	##2014-11-25T15:00:00-05:00
	##2014-12-18T13:10:25-05:00
	return re.sub(r'[-|+]\d+:\d+\S$', "",timeStr)

##return a number or None
def timeToTimeStamp(timeStr):
	##2014-11-22T16:23:15-0500
	##The 2nd part (-0500) is actually showing what time zone you are in. That means that you are 5 hours behind Greenwich Mean Time (also known as UTC). 
	##-0500 right now is US Central Time. 

	##2015-02-11
	
	local = pytz.timezone ("US/Eastern")
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	naive = None
	if len(timeStr) > len("2015-02-11"):
		formattedTimeStr = formatAtlanticString(timeStr)
		naive = datetime.datetime.strptime (formattedTimeStr, "%Y-%m-%dT%H:%M:%S")
	elif len(timeStr) == len("2015-02-11"):
		naive = datetime.datetime.strptime (timeStr, "%Y-%m-%d")
	else:
		return 0



	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	print timeStamp
	return timeStamp

