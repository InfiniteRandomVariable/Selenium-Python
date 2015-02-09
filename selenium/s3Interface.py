from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os, re, jsonHelper
import os.path
import time
from time import mktime
import datetime



#ABS_PATH = '~/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium'
CRED = '.s3'
ACCESS = 'accesskey'
SECRET = 'secret'
BUCKET_NAME = 'data.hotoppy.com'
IMAGE_PATH = '/imaging/images'
SECONDS_IN_A_DAY = 24 * 60 * 60
OneAndHalfDay = SECONDS_IN_A_DAY * 2
#OneAndHalfDay = 1
UPLOAD_SUFFIX = 'uploaded'
#IMAGE_KEY_SUBFOLDER = "images/"
IMAGE_KEY_SUBFOLDER = "i/"
#TEMP_PATH = 'guardian/1420592.json'

def imagePath():
	return IMAGE_PATH

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
# minor error [Errno 1] Operation not permitted: '/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images'
# possible fix: http://stackoverflow.com/questions/10937806/oserror-error-1-operation-not-permitted
# chown -R username:groupname .

def sendData( localPath, buckName=None, forwardWrite=24):
	
	#thelocalPath = "{0}".format( localpath )
	#print "localPath 1 %s" % localPath

	if not buckName or len(buckName) < 1:
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



		
		if len(localPath) < 7 or len(localPathArray) < 2:
			print("Error check localpath {0}".format(localpath))
			return;


		if IMAGE_PATH in localPath:
		 	##image Operation
		 	topdir = '.{0}'.format(IMAGE_PATH)
		# 	# The arg argument for walk, and subsequently ext for step
			exten = '.jpg'
			#imageNameList = [v.name[len("images/"):] for v in list(b.list("images/", "/"))]
			imageNameList = [v.name[len(IMAGE_KEY_SUBFOLDER):] for v in list(b.list(IMAGE_KEY_SUBFOLDER, "/"))]
			# print("imageName: {0}".format(imageNameList[4]) )

			uploadSuffixSubstringHelper = -len(UPLOAD_SUFFIX)

			def step(ext, dirname, names):
				#global _localPath

				ext = ext.lower()
				print("0 ext: {0}".format(ext))
				dt = datetime.datetime.now()
				print("1")
				nowInSeconds = time.mktime(dt.timetuple())

				print("2")

				for name in names:

					if len(name) <2:
						continue

#					if name.lower().endswith(ext) is False:
#						continue
					
					#print("name[:-len(UPLOAD_SUFFIX)]: {0}".format(name[:-(len(UPLOAD_SUFFIX)]))
					print("3 try: {0}".format(name[:uploadSuffixSubstringHelper]))

					if name.lower().endswith(ext) is True and name not in imageNameList:
						print("4")
						keyName = "{0}{1}".format(IMAGE_KEY_SUBFOLDER, name)
						print("2 keyName: {0}".format(keyName))
						imagekey = b.new_key(keyName)

						print("Uploading file name: {0}".format(name))

						imagekey.Content_Type = "image/jpeg"

						try:
							pathToImageFile = "{0}/{1}".format(localPath,name)
							imagekey.set_contents_from_filename(pathToImageFile)
							imagekey.make_public()
							localPathExt = "{0}{1}".format(pathToImageFile, UPLOAD_SUFFIX)
							os.rename(pathToImageFile, localPathExt)

						except Exception as e:
							print("Exception uploading image: {0} - {1}".format(keyName, e))

					elif name.lower().endswith(UPLOAD_SUFFIX) is True and name[:uploadSuffixSubstringHelper] in imageNameList:

						keyName = "{0}{1}".format(IMAGE_KEY_SUBFOLDER,name[:uploadSuffixSubstringHelper])
						imagekey = b.get_key(keyName)
						print("Not Uploading file name: {0} last-modified: {1}".format(keyName, imagekey.last_modified))
						##"Thu Jan 29 19:13:17 GMT-800 2015"

						# print("imageNameList: {0}".format(imageNameList[0]))

						modified = time.strptime(imagekey.last_modified, '%a, %d %b %Y %H:%M:%S %Z')

						#convert to datetime
						print("time date 0")
						mdt = datetime.datetime.fromtimestamp(mktime(modified))
						print("time date 1")
						#(dt.datetime(1970,1,1)).total_seconds()
						
						#modifiedTimeInSeconds = mdt.datetime(1970,1,1).total_seconds()
						modifiedTimeInSeconds = time.mktime(mdt.timetuple())
						print("time date 2")

						durationInSeconds = nowInSeconds - modifiedTimeInSeconds
						systemPath = jsonHelper.getCompleteFilePath()
						print("should delete: {0}{1}/{2}".format(systemPath, dirname[1:], name))
						#os.remove(localPath)
						#assume default dirname is "./xyz"
						deleteFilePath = "{0}{1}/{2}".format(systemPath, dirname[1:], name))

						if durationInSeconds > OneAndHalfDay and len(imageNameList) > 0:
							try:
								b.delete_key(imagekey)
								#os.remove(deleteFilePath)
							except Exception as e:
								print ("Exception in deleting key: {0} - {1}".format(imagekey, e))

			os.path.walk(topdir, step, exten)


		else:

			##JSON Operation	
			
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
		#print("should delete: {0}".format(localpath))
		#os.remove(localPath)

	except Exception as e:
		print(e)
	#	print "ERROR s3Interface %s" % e

def uploadImagesProcedure():
	imagePath = jsonHelper.getCompleteFilePath('imaging', 'images')
	sendData(imagePath)

