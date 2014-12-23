import unittest
import pytz, datetime
import calendar
import re

def formatString(timeStr):
	## change to r'[-|+]\d\S$'
	regex_hour_selector = r'\s(\d+):'
	searchObj = re.search( regex_hour_selector, timeStr).group()
	hours = int(re.sub(r':$',"",searchObj.strip()))
	
	PMorAM = re.search('p\.?m\.?|a\.?M\.?', timeStr, re.IGNORECASE).group().strip()
	#remove the am or pm from the str
	if 'p' in PMorAM or 'P' in PMorAM:
		#add 12 hours
		hours = hours + 12
	elif hours < 10 :
		hours = "0%s" % hours
	
	hoursString = " %s:" % hours
		
	#print 'PMorAM %s\nHours: %s' % (PMorAM, hoursString)

	regex = r"%s" % PMorAM
	_timeStr =  re.sub(regex, "",timeStr)
	ft0 = re.sub(regex_hour_selector,hoursString,_timeStr)
	ft1 = re.sub(r'Updated','',ft0, re.IGNORECASE)
	ft2 = re.sub(r'ET','',ft1,re.IGNORECASE)
	#print "Final time: %s" % ft2
	return ft2.strip()


def timeToTimeStamp(timeStr):
	
	timeZONE = 'US/Eastern'
	if 'ET' in timeStr == False or 'Ea' in timeStr == False:
		timeZONE = 'US/Pacific'


	##Dec. 14, 2014 11:12 p.m. ET
	
	local = pytz.timezone (timeZONE)
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	formattedTimeStr = formatString(timeStr)
	#Dec. 14, 2014 13:12  ET
	naive = datetime.datetime.strptime (formattedTimeStr, "%b. %d, %Y %H:%M")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	#print timeStamp
	return timeStamp