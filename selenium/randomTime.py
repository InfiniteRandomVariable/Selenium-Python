import random

def randomTime(totalNum):
	totalSeconds = 0
	for x in range(totalNum):
		totalSeconds = random.random() + totalSeconds

	return int(totalSeconds)
