import unittest
import pytz, datetime
import calendar
import re

def formatGuardianString(timeStr):
	return re.sub(r'[-|+]\d\d\d\d$', "",timeStr)

def guardianTimeToTimeStamp(timeStr):
	
	##GURDIAN TIME STAMP STRING
	##2014-11-22T16:23:15-0500
	
	local = pytz.timezone ("US/Eastern")
	##Python 2.7 Bug with %z. Fixed Python 3.x
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	formattedTimeStr = formatGuardianString(timeStr)
	naive = datetime.datetime.strptime (formattedTimeStr, "%Y-%m-%dT%H:%M:%S")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	print timeStamp
	return timeStamp

class PythonOrgSearch(unittest.TestCase):

	guardianTimeToTimeStamp("2014-11-22T16:23:15")

if __name__ == "__main__":
    unittest.main()