import json, io, os, random, common_classes, errno, s3Interface
from json import dumps

#from collections import OrderedDict

class A(object):
	def __init__(self):
		self.b_list = []


#class B(object):
#	def __init__(self):
#		self.x = 'X'
#		self.y = random.random()

def encode_b(obj):
	if isinstance(obj, common_classes.Article):
		return obj.__dict__
	return obj

#url, title, numComments


#json.dumps(a, default=encode_b)
def writeToFile(timestamp,listObjects,publication,min_articles=2):

	if len(listObjects) < min_articles:
		return
	if isinstance(listObjects,list) == False:
		raise Exception("Should be an article list")
	if isinstance(timestamp, int) == False:
		raise Exception("Should be a timestamp")

	if not os.path.isdir("%s" % publication) :
		try:
			os.makedirs(publication)
		except:
			if e.errno != errno.EEXIST:
				raise e
			pass

	a = A()
	a.b_list = listObjects
	dataFileName = '%s.json' % timestamp
	
	#fileName = os.path.join(publication,dataFileName)
	
	fileName = getCompleteFilePath(publication,dataFileName)
	aDict = a.__dict__
	aDict[publication] = aDict.pop('b_list')
	
	with io.open(fileName, 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(aDict, default=encode_b,encoding="utf-8",ensure_ascii=False,indent=1)))
	#	f.write(unicode(json.dumps(aDict, default=encode_b,encoding="utf-8",ensure_ascii=False,indent=1)))

	s3Interface.sendData(fileName)

def getCompleteFilePath(*arg):
	return os.path.join(os.path.expanduser('~'), 'Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium', *arg)
	

		#f.write(unicode(json.dumps(a.__dict__, default=encode_b,encoding="utf-8",ensure_ascii=False,indent=1)))

#	print 'JSON: %s' % json.dumps(a.__dict__, default=encode_b,indent=1, ensure_ascii=False)

#theList = []
#for i in range(10):
#	theList.append(common_classes.Article('URL'))
#writeToFile(200, theList)

