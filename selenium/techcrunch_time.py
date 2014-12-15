import pytz, datetime
import calendar
import re

def formatAtlanticString(timeStr):
	##2014-11-25T15:00:00-05:00
	return re.sub(r'[-|+]\d+:\d+\S$', "",timeStr)

def timeToTimeStamp(timeStr):
	
	##GURDIAN TIME STAMP STRING
	##2014-11-22T16:23:15-0500
	##The 2nd part (-0500) is actually showing what time zone you are in. That means that you are 5 hours behind Greenwich Mean Time (also known as UTC). 
	##-0500 right now is US Central Time. 

	#eg. timestamp timeStr= "2014-12-14 11:05:12"
	local = pytz.timezone ("US/Pacific")
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	#formattedTimeStr = formatAtlanticString(timeStr)

	naive = datetime.datetime.strptime (timeStr, "%Y-%m-%d %H:%M:%S")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	print timeStamp
	return timeStamp

