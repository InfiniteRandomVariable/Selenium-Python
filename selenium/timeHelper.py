from datetime import datetime
import calendar

def sortTimeForGuardian(timeList):
	return timeList.sort(key=lambda x: x.age, reverse=True)

def TIME_UTC_LINUX():
	d = datetime.utcnow()
	return calendar.timegm(d.utctimetuple())

def TIME_UTC_LINUX_DIVIDER(timeDivider=1):
	return TIME_UTC_LINUX()/timeDivider

def APP_TIMESTAMP():
	return TIME_UTC_LINUX_DIVIDER(1000)

#if __name__ == "__main__":
#	print 'TIME: %s' % APP_TIMESTAMP()

    #unittest.main()
    
# # To sort the list in place...
# ut.sort(key=lambda x: x.count, reverse=True)

# # To return a new list, use the sorted() built-in function...
# newlist = sorted(ut, key=lambda x: x.count, reverse=True)

#JAVASCRIPT UTC TIME
#var v = new Date().getTime();
#    window.alert(parseInt(v/1000000));