import re, os
from PIL import Image
import requests
from StringIO import StringIO
import jsonHelper, common_classes
import imghdr, requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import s3Interface


##require contain jpg or jpeg in the file 
def matchURLEndJPG(url):
	searchObj = re.search(r'.+?(?=\.jpe?g)', url , re.I)
	if '.jpg' in url:
		return "{0}{1}".format(searchObj.group(),'.jpg')
	elif '.jpeg' in url:
		return "{0}{1}".format(searchObj.group(),'.jpeg')
	else:
		raise ValueError("Error matchURLUtilJPG: {0}".format(url))
		return ""


#http://stackoverflow.com/questions/19532125/cant-install-pil-after-mac-os-x-10-9
def imageURLformatter(url, maxStringLength=9):
	urlStr = re.sub(r'^h?t?t?p?s?\:?\/?\/',"", url.strip(), re.I)
	print (urlStr)
	urlLen = len(urlStr) - maxStringLength
	dashURL = re.sub(r'[^\w]',"-", urlStr[urlLen:])
	print (dashURL)
	fURL = re.sub(r'[^\w]+$', "", dashURL)
	print(fURL)
	return fURL

# def imageURLJPG(url):
# 	return "{0}.{1}".format(url,'jpg')

# def imageURL_type(url, ext):
# 	return "{0}.{1}".format(url,ext)

#get the image to PIL Image
#use this im.verify() to verify the file
#save the image to local storage as pendingimage
#identifyfiletype (optional)
#process the article URL
#append the image file extension to the processed article URL name (optional)
#rename the image in the local storage (optional)


	#http://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
	#http://stackoverflow.com/questions/19230991/image-open-cannot-identify-image-file-python
	#http://effbot.org/imagingbook/image.htm
	#https://docs.python.org/2/library/imghdr.html

def imageTitlePathJPG(title):
		return "i/{0}{1}".format(imageURLformatter(title), '.jpg')

def imageTitlePathWithSupportType(title, ext):
		searchObj = re.search( r'(jpg|jpeg|png|gif)', ext, re.I)
		if searchObj:
			fExt = searchObj.group().lower()
			if fExt in 'jpeg':
				fExt = 'jpg'
			return "i/{0}.{1}".format(imageURLformatter(title), fExt)

		else:
			raise ValueError("suport format: {0}".format(ext))
			return ""


def imageFilePath():
	return jsonHelper.getCompleteFilePath("imaging", "images")

def imageURI(title):
	print("3.1")
	imageURI = imageURLformatter(title)
	if not len(imageURI) > 1:
		print("3.2")
		return ""

	print("3.3")
	systemPath = imageFilePath()
	print("3.4 system Path: {0}".format(systemPath))
	return "{0}/{1}".format(systemPath, imageURI)

def getQualifyImgExt(url):
	searchObj = re.search( r'(jpg|jpeg|png|gif|tiff|bmp)', url, re.I)
	if not searchObj:
		print ('getImageAndSave nil URL')
		return ""

	return searchObj.group().lower()

## don't change the extension type in the save operation
## the bash script will convert to jpg format
## the cloud will expect image with jpg extension.

def getImageAndSave(url, articleTitle):

	try:

		ext = getQualifyImgExt(url)
		if ext == 'jpeg':
			ext = 'jpg'
		elif not len(ext) > 1:
			return False

		print("getImageAndSave 0")
		response = requests.get(url)
		print("getImageAndSave 1")
		img = Image.open(StringIO(response.content))
		print("getImageAndSave 2")
		img.verify()
		print("3")
		img = Image.open(StringIO(response.content))
 		localURI = "{0}.{1}".format(imageURI(articleTitle), ext)
 		print("4")
 		if len(localURI) > 5:
 			print("5 localURL: {0}".format(localURI))
			img.save(localURI)
			print("6")
			imageType = imghdr.what(localURI).lower()
			print("7")
			match = re.match( r'(png|gif|tiff|bmp)', imageType , re.I)
			print("8")
			if imageType == 'jpeg' or imageType == 'jpg':
				print("8.1")
				imageType = 'jpg'
			elif match and len (match.group()) > 1:
				print("8.2")
				imageType  = match.group().lower()
			else:
				print("8.3")
				os.remove(localURI)
				return False
			print("9")

			if imageType is not ext:
				reExt =r'{0}$'.format(ext)
				localPathExt =re.sub(reExt, imageType, localURI)
				os.rename(localURI, localPathExt)
				return True
			else:
				return True


	except Exception as e:
		print("Get IMAGE ERROR: {0}".format(e))
		return False


#".image img"
#"img.media-viewer-candidate"
#"src"

def isImageExistLocally(title):
	imgTitle = imageURLformatter(title);
	global isMatch
	isMatch = False

	if not len(imgTitle) > 1:
		return isMatch

	IMAGE_PATH = s3Interface.imagePath()
	topdir = ".{0}".format(IMAGE_PATH)
	
	def step(ext, dirname, names):
		global isMatch
		for name in names:
			print("imageTitle: {0} name: {1}".format(imgTitle, name))
			if imgTitle in name:
				isMatch = True
				#print("isMatch 1:  {0}".format(isMatch))
				return isMatch
		#print("isMatch 2:  {0}".format(isMatch))				
		return isMatch

	os.path.walk(topdir, step, 'jpg')
	#print("isMatch 4: {0}".format(isMatch))

	return isMatch

def getURL(url):
	return re.search(r'h?t?t?p?s?:?//.+[\w]', url, re.I)


## if success, it should return a non empty string presenting the img ext
def imageProcedure(driver, title , cssXpaths=[],  webElement=None ):
	if not isinstance( driver, WebDriver):
		raise ValueError("Must be seleniumDriver")

	isSuccess = False
	print "0 imageProcedure"

	if len(title ) > 2:

		imageURL = ""

		print "1 imageProcedure"
		isExist = isImageExistLocally(title)

		if isExist:
			print("is exist: {0}".format(title))
			return isExist

		
		if not isinstance(cssXpaths, list):
			raise ValueError("must be list or CSSXPATH")

		# for cssXpath in arg:
		# if isinstance(cssXpath, list):
		# 		cssXpaths = cssXpath
		# 	elif isinstance(cssXpath, common_classes.CSSXPATH):
		# 		cssXpaths = arg
		# 	else:
		# 		raise ValueError("must be list or CSSXPATH")
		# 		return isSuccess


		for cssXpath in cssXpaths[:]:

			#print("2 {0}".format(cssXpath))
			if not isinstance(cssXpath, common_classes.CSSXPATH):
				raise ValueError("must be list or CSSXPATH")

			elememt = None
			try:
				if cssXpath.pathType == 'css' or webElement:
					print("css section URL:{0} attribute: {1} path: {2}".format(imageURL, cssXpath.attribute, cssXpath.path))

					if webElement:
						elememt = webElement
					else:
						elememt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, cssXpath.path)))

					imageURL = elememt.get_attribute(cssXpath.attribute)
					imageURLResult = getURL(imageURL)
					if imageURLResult: 
						imageURL = matchURLEndJPG(imageURLResult.group())
					if len(imageURL) < 2:
						imageURL = imageURLResult.group()
					##wsj "background-image:url(http://m.wsj.net/video/20150205/020415pathomap1/020415pathomap1_960x540.jpg)"

					print("css section URL:{0} attribute: {1} path: {2}".format(imageURL, cssXpath.attribute, cssXpath.path))
				elif cssXpath.pathType == 'xpath':
					print("xpath section {0} attribute: {1} path: {2}".format(imageURL, cssXpath.attribute, cssXpath.path))
					elememt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cssXpath.path)))
					imageURL = elememt.get_attribute(cssXpath.attribute)
					print("xpath section {0} attribute: {1} path: {2}".format(imageURL, cssXpath.attribute, cssXpath.path))
			except Exception as e:
				continue 

			if len(imageURL) > 0:
				print("about to call get Image and save {0}".format(imageURL))
				isSuccess = getImageAndSave(imageURL, title)
				print("about to call get Image and save {0}".format(isSuccess))
				if isSuccess:
					return getQualifyImgExt(imageURL)

		return isSuccess

	else:
		return isSuccess




