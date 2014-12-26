
import unittest



def printIntervals(intervalMins, hours):

	sixtyMins = 60
	minutes = 0
	hoursInMins = hours * sixtyMins
	currentMins = 0

	timeLogs = []
	firstScriptMin = ''
	secondScriptMin = ''
	thirdScriptMin = ''

	firstScriptHour = ''
	secondScriptHour = ''
	thirdScriptHour = ''

	scriptMonitor = 0

	
	while currentMins < hoursInMins:

		
		currentMins = currentMins + intervalMins
		hours = int(currentMins/sixtyMins)
		mins = currentMins % sixtyMins
		# if mins == 0:
		# 	mins = "00"

		timeLogStr = "%s:%s" % (hours, mins)

		if scriptMonitor == 0:
			scriptMonitor = scriptMonitor + 1
			if len(firstScriptMin) == 0:
				firstScriptMin = "%s" % (mins)
			else:
				firstScriptMin = "%s,%s" %(firstScriptMin,mins)

			if len(firstScriptHour) == 0:
				firstScriptHour = "%s" % (hours)
			else:
				firstScriptHour = "%s,%s" %(firstScriptHour,hours)


		elif scriptMonitor == 1:
			scriptMonitor = scriptMonitor + 1

			if len(secondScriptMin) == 0:
				secondScriptMin = "%s" % (mins)
			else:
				secondScriptMin = "%s,%s" %(secondScriptMin,mins)

			if len(secondScriptHour) == 0:
				secondScriptHour = "%s" % (hours)
			else:
				secondScriptHour = "%s,%s" %(secondScriptHour,hours)



		elif scriptMonitor == 2:
			scriptMonitor = 0
			if len(thirdScriptMin) == 0:
				thirdScriptMin = "%s" % (mins)
			else:
				thirdScriptMin = "%s,%s" %(thirdScriptMin,mins)

			if len(thirdScriptHour) == 0:
				thirdScriptHour = "%s" % (hours)
			else:
				thirdScriptHour = "%s,%s" %(thirdScriptHour,hours)



		timeLogs.append(timeLogStr)

	print timeLogs
	print "FIRST HOURS: %s" % firstScriptHour
	print "FIRST MINS: %s" % firstScriptMin

	print "SECOND HOURS: %s" % secondScriptHour
	print "SECOND MINS: %s" % secondScriptMin

	print "THIRD HOURS: %s" % thirdScriptHour
	print "THIRD MINS: %s" % thirdScriptMin		


class CronJobScripter(unittest.TestCase):

	printIntervals(40,24)

if __name__ == "__main__":
    unittest.main()


# FIRST HOURS: 0,2,4,6,8,10,12,14,16,18,20,22
# FIRST MINS: 40,40,40,40,40,40,40,40,40,40,40,40
# SECOND HOURS: 1,3,5,7,9,11,13,15,17,19,21,23
# SECOND MINS: 20,20,20,20,20,20,20,20,20,20,20,20
# THIRD HOURS: 2,4,6,8,10,12,14,16,18,20,22,24
# THIRD MINS: 0,0,0,0,0,0,0,0,0,0,0,0