from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os, re, jsonHelper


#ABS_PATH = '~/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium'
CRED = '.s3'
ACCESS = 'accesskey'
SECRET = 'secret'
BUCKET_NAME = 'data.hotoppy.com'
#TEMP_PATH = 'guardian/1420592.json'

def readCred():
	if len(CRED) < 1:
		#print "please provide the credential file name"
		return 
	counter = 0
	cred_path = jsonHelper.getCompleteFilePath(CRED)
	dictCred = { ACCESS: '' , SECRET: '' }
	with open(cred_path) as f:
		content = f.read().splitlines()
		dictCred[ACCESS] = content[counter]
		counter = counter + 1
		dictCred[SECRET] = content[counter]
		print content
		return dictCred

#NOTE: the S3 path will be lower case where local file name maybe upper case
#Parameters: forwardWrite default to 5 to ensure continuity of the data for upcoming event and expected the newer data will overwrite this
#			  localPath, consist of this pattern publicationName/timestamp.json
#			

def sendData( localPath, buckName=None, forwardWrite=24):

	#print "localPath 1 %s" % localPath

	if not buckName or len(buckName) < 1 :
		buckName = BUCKET_NAME
		#return

	if len (localPath) < 1:
		return


	try:
		cred = readCred()
		conn = S3Connection(cred[ACCESS], cred[SECRET])
		b = None
		try:
			b = conn.get_bucket(buckName)
		except Exception as e:
			b = conn.create_bucket(buckName)

		if not b:
			#print "Error: bucket cannot be nil"
			return

		systemPath = jsonHelper.getCompleteFilePath().lower().split('/')
		localPathArray = localPath.lower().split('/')
		print("systemPath: {0}, localPath: {1}".format(systemPath, localPathArray))

		for pathIndex in range(len(systemPath)):
			pathStr = systemPath[pathIndex]
			if pathStr.find(localPathArray[pathIndex]) < 0:
				print("NOT MATCH Path name s3Interface: {0}".format(localPathArray[pathIndex]))
				return


		#re.sub(r'\.json$',"",localPath.lower())
		#strippedPath = re.sub(r'\.json$',"",localPath.lower())
		timeName = localPathArray[len(localPathArray)-1]
		strippedPath = re.sub(r'\.json$',"",timeName.lower())
		timeStampStr = re.search( r'\d+$', strippedPath).group()
				
		timestamp = int(timeStampStr)	

		print 'strippedPath ' + strippedPath
		#publicationName = re.search( r'^\w+', strippedPath).group()

		publicationName = localPathArray[len(localPathArray)-2]
		print('publicationName {0}'.format(publicationName))
		if timestamp < 100 and len(publicationName) < 1:
			#print "error in publication name or time stamp"
			return

		# metaData = {'charset': 'utf-8', 'Content-Type': 'application/json; '}
		k = Key(b)
		# k.metadata = metaData
		k.Content_Type = 'application/json; charset=utf-8'
		k.content_disposition = 'inline'
		# k.content_encoding = 'gzip'

		for num in range(forwardWrite):

			if num == 0:

				k.key = "%s/%d.json" % (publicationName, timestamp)
				k.set_contents_from_filename(localPath)
				k.make_public()

			else:
				k.copy(buckName,"%s/%d.json" % (publicationName, timestamp)).make_public()

			
			timestamp = timestamp + 1		
		os.remove(localPath)

	except Exception as e:
		print(e)
	#	print "ERROR s3Interface %s" % e
