from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time, articleUtil, imageUtil
import pytz, datetime
import calendar
import re
import randomTime
import sys




##PROBLEM
## only can find the first 4 items. Maybe memory problem?
##http://static01.nyt.com/images/2015/02/01/world/JUSTICE/JUSTICE-facebookJumbo.jpg
##http://static01.nyt.com/images/2015/02/01/world/JUSTICE/JUSTICE-master675.jpg
def timeToTimeStamp(timeStr):
	##2015-01-23T10:30:58+00:00
	timeZONE = 'US/Eastern'
	##naive = datetime.datetime.strptime (formattedTimeStr, "%Y-%m-%dT%H:%M")
	SAMPLE_FROM_PUB = "2014-12-22"
	##2014-12-22
	local = pytz.timezone (timeZONE)
	timeFormat = ""

	if len(timeStr) > len(SAMPLE_FROM_PUB):
		timeFormat = "%Y-%m-%dT%H:%M:%S"
	else:
		timeFormat = "%Y-%m-%d"

	naive = datetime.datetime.strptime (timeStr,timeFormat)
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	#print timeStamp
	return timeStamp



browser = webdriver.Firefox()

NAME='nytimes' 
BASE= 'http://www.%s.com' % NAME 

WEBSITE_URL = '%s' % BASE

#browser.get(WEBSITE_URL)
#browser.get('http://www.nytimes.com/most-popular')
browser.get('https://myaccount.nytimes.com/auth/login?URI=http://www.nytimes.com/most-popular')

rowElements = []
divider = 6
MIN_LIKES = 30/divider
MIN_COMMENT_NUM = 100/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=7
WAIT_SECONDS = 3

POPULARS = '//ol/li/a'
SEARCH_START = 10
SEARCH_END = 19






#id input#userid
#id input#password
# button#js-login-submit-button

#step 1
#log-in


#.button.login-button.login-modal-trigger
#input#login-password
#input#login-email
#button#login-send-button

time.sleep(randomTime.randomTime(5))
pages=[]

try:
	print "1"
	#WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.button.login-button'))).click()
	print "2"
	WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input#userid'))).send_keys('lauyukpui@yahoo.com')
	print "3"
	time.sleep(randomTime.randomTime(3))
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input#password'))).send_keys('NYTIMES2014')
	print "4"
	time.sleep(randomTime.randomTime(5))
	print "KILL process"
	WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#js-login-submit-button'))).click()

except Exception as e:
	print "LOGIN Exception: %s" % e

# sys.exit()

#//ol/li/a
#//ol/li/a[@href]

try:
	print "11"

	
	popularElms = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH,POPULARS)))[SEARCH_START:SEARCH_END]

	for pE in popularElms[:]:
		print "12"
		_url = pE.get_attribute('href')
		url = re.sub(r'\?src=mv',"",_url)
		print "13"
		if 'interactive' in url:
			print "BLOCKED URL: %s" % url
			continue
		a = common_classes.Article(url)
		a.title = pE.text.strip()

		print "Title: %s" % a.title
		if len(a.title) < 4:
			continue

		urlWithoutArticleLink = re.sub(r'\/?[\=\?\w\.\-]+$',"",a.url)
		print "URL: %s" % a.url
		try:
			a.tag = re.search(r'[\w]+$', urlWithoutArticleLink).group()
			print "TAG: %s" % a.tag
		except Exception as ee:
			a.tag = NAME

		pages.append(a)
	

except Exception as e:
	print "PopularPage %s" % e

#https://myaccount.nytimes.com/auth/login?URI=http://www.nytimes.com/most-popular

isFirstPage = True
	#print "6"
for article in pages[:]:

	browser.get(article.url)
	if isFirstPage == False:
		time.sleep(WAIT_SECONDS)
	isFirstPage = False
	try:
		commentButton = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.button.comments-button.theme-kicker')))
	except Exception as e:
		print "Exception commentButton: %s" % e
		continue

	try:
		numCommentText = commentButton.find_element_by_css_selector('.count').text.strip()
		print "numComments: %s" % numCommentText
		article.numComments = int(numCommentText)
		commentButton.click()
	except Exception as e:
	 	article.numComments = 1
	 	print "Exception numComments: %s" % e
	 	continue

	

	time.sleep(WAIT_SECONDS)

	try:
		WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.tab.reader'))).click()
		time.sleep(WAIT_SECONDS*2)
		article.topComment = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.comments-view.tab-content .comment-text'))).text
		article.topComment = articleUtil.truncatedStringForRow(article.topComment)
		# if len(article.topComment) > (WORDS_LIMIT -2):
		# 	tpC = re.sub(r'\.*$',"",article.topComment)
		# 	article.topComment = "%s..." % tpC

		print "topComment %s" % article.topComment
		article.topCommentNum = int(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.recommend-count'))).text.strip())
		print "topCommentNum %s" % article.topCommentNum
		timeText = str(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.dateline'))).get_attribute('datetime')).strip()
		print "timeText1 %s" % timeText
		timeText = re.search(r'^[^+]+',timeText).group()
		print "timeText2 %s" % timeText

		##article.age = int(timeToTimeStamp(timeText))/1000
		article.age = int(timeToTimeStamp(timeText)) - len(rowElements)
		print "article.age %s" % article.age	

	except Exception as e:
		print "Exception: %s" % e
		continue
	
	#article.tag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".blogName>a"))).text.strip()
	#figure.media .image.img
	#.thumb img
	print("about to call getImageAndSave")
	isSuccess = imageUtil.imageProcedure(browser, article.title, [ common_classes.CSSXPATH("figure.media .image.img", "src", "css"), common_classes.CSSXPATH(".image img", "src", "css"), common_classes.CSSXPATH("#story-body .thumb img", "src", "css"), common_classes.CSSXPATH("img.media-viewer-candidate", "src", "css")])
	print("return from getImageAndSave")        
	article.img = imageUtil.imageTitlePathJPG(article.title)

	if isSuccess and len(article.img) > 1 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10 and article.topCommentNum > MIN_LIKES:
		rowElements.append(article)
	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s article.topCommentNum %s " %( article.title,article.topComment, article.url, article.age, article.topCommentNum)
		pass


jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
browser.quit()


