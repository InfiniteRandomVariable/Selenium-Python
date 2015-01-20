from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time, articleUtil
import pytz, datetime
import calendar
import re


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

def timeToTimeStamp(timeStr):
	
	timeZONE = 'US/Pacific'

	##Published on Dec 21, 2014
	local = pytz.timezone (timeZONE)
	##naive = datetime.datetime.strptime (timeStr, "%Y-%m-%dT%H:%M:%S%z")
	formattedTimeStr = re.sub(r'^Published on\s?', "", timeStr.strip())
	#Dec. 14, 2014 13:12  ET
	#Dec 21, 2014
	naive = datetime.datetime.strptime (formattedTimeStr, "%b %d, %Y")

	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	#print timeStamp
	return timeStamp


browser = webdriver.Firefox()

NAME='youtube' 
BASE= 'http://www.%s.com' % NAME 

WEBSITE_URL = '%s/channel/UCF0pVplsI8R5kcAqgtoRqoA' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 1
MIN_LIKES = 30/divider
MIN_COMMENT_NUM = 100/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=5
WAIT_SECONDS = 3

POPULARS = '.yt-uix-sessionlink.yt-uix-tile-link'

pages=[]
try:
	
	rows = WebDriverWait(browser, 25).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,POPULARS)))[0:MAX_RANKING]

	for row in rows[:]:

		a = common_classes.Article(row.get_attribute('href'))
		if len(a.url) > 5:
			pages.append(a)

		#print "URL %s" % a.url

except Exception as e:
	print(e)
	#print "Exception: failure in bloomberg \n%s" % e

isFirstPage = True
for article in pages[:]:
	#print "6"
	url = "%s%s" %(article.url, '#disqus_thread')
	browser.get(url)
	if isFirstPage == False:
		time.sleep(WAIT_SECONDS)
	isFirstPage = False

#article.tag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".blogName>a"))).text.strip()
	
	try:

		article.title = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID,'eow-title'))).text.decode('utf-8', errors='ignore').strip()
		print(type(article.title)) 
		timeText  = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".watch-time-text"))).text
		#article.age = int(theTimeStampText)/1000
		article.age = timeToTimeStamp(timeText)/1000
		if article.age == None or article.title == None or article.age < 10 or len(article.title) < 2:
			#print "timestamp length %s\n title:%s " % (article.age, article.title)
			continue
		#print "timeStamp: %s" % article.age
	except Exception as e:
		print(e)
		browser.switch_to.default_content()
		continue

	frame = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.comments-iframe-container>div>iframe')))

	browser.switch_to.frame(frame)
	numCommentText = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.DJa'))).text.strip()

	article.numComments = int(re.sub(r'\D', "", numCommentText).strip())
	#print "commentNum: %s commentNumText: %s" % (numCommentText,article.numComments)
	if article.numComments < MIN_COMMENT_NUM:
		#print "CONTINUE: comment number is too low"
		browser.switch_to.default_content()
		continue

	article.topComment = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.Ct'))).text
	article.topComment = articleUtil.truncatedStringForRow(article.topComment)

	print(type(article.topComment))

	article.topCommentNum = int(WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.uPc.bmd'))).text.strip())
	browser.switch_to.default_content()
	article.tag = 'video'


	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10 and article.topCommentNum > MIN_LIKES:
		rowElements.append(article)
	else:
		#print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s article.topCommentNum %s " %( article.title,article.topComment, article.url, article.age, article.topCommentNum)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
browser.quit()
