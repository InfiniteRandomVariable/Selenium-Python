
def sortTimeForGuardian(timeList):
	return timeList.sort(key=lambda x: x.age, reverse=True)

# # To sort the list in place...
# ut.sort(key=lambda x: x.count, reverse=True)

# # To return a new list, use the sorted() built-in function...
# newlist = sorted(ut, key=lambda x: x.count, reverse=True)