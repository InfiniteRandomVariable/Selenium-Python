from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time, articleUtil
import pytz, datetime
import calendar
import re, imageUtil


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
divider = 10
MIN_LIKES = 30/divider
MIN_COMMENT_NUM = 100/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=5
WAIT_SECONDS = 3

POPULARS = '.yt-uix-sessionlink.yt-uix-tile-link'
THUMB_PATH = '.yt-thumb-clip>img'

pages=[]
try:
	
	topElm = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.ID,"browse-items-primary")))

	rows = topElm.find_elements_by_css_selector(POPULARS)[0:MAX_RANKING]
	imgRows = topElm.find_elements_by_css_selector(THUMB_PATH)[0:MAX_RANKING]

	for index in range(len(rows)):
		row = rows[index]
		iRow = None

		if len(imgRows) > index:
			iRow = imgRows[index]


	#for row in rows[:]:

		a = common_classes.Article(row.get_attribute('href'))
		a.title = row.get_attribute('title')
		if len(a.url) > 5 and iRow:
			isSuccess = imageUtil.imageProcedure(browser, a.title , cssXpaths=[common_classes.CSSXPATH(THUMB_PATH, "src", "css")] , webElement=iRow)
			a.img = imageUtil.imageTitlePathJPG(a.title)
			if isSuccess and len(a.img) > 2:
				pages.append(a)



except Exception as e:
	print("Exception: topElm {0}".format(e))
	#print "Exception: failure in bloomberg \n%s" % e


for article in pages[:]:
	#print "6"
	url = "%s%s" %(article.url, '#disqus_thread')
	browser.get(url)
	
	time.sleep(WAIT_SECONDS)
	

#article.tag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".blogName>a"))).text.strip()
	
	try:

		#uni code error? and random symbols?
		#article.title = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID,'eow-title'))).text.decode('utf-8', errors='ignore').strip()
		#print(type(article.title)) 
		timeText  = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".watch-time-text"))).text
		#article.age = int(theTimeStampText)/1000
		article.age = timeToTimeStamp(timeText)
		if article.age == None or article.title == None or article.age < 10 or len(article.title) < 2:
			#print "timestamp length %s\n title:%s " % (article.age, article.title)
			continue
		#print "timeStamp: %s" % article.age
	except Exception as e:
		print("Exception youtube0 {0}".format(e))
		browser.switch_to.default_content()
		continue

	try:

		frame = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.comments-iframe-container>div>iframe')))
		browser.switch_to.frame(frame)
		time.sleep(WAIT_SECONDS)
		numCommentText = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.DJa'))).text.strip()
		article.numComments = int(re.sub(r'\D', "", numCommentText).strip())

	except Exception as e:
		print("Exception youtube1 {0}".format(e))
		continue



	#print "commentNum: %s commentNumText: %s" % (numCommentText,article.numComments)
	if article.numComments < MIN_COMMENT_NUM:
		#print "CONTINUE: comment number is too low"
		browser.switch_to.default_content()
		continue

	try:

		article.topComment = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.Ct'))).text
		article.topComment = articleUtil.truncatedStringForRow(article.topComment)

	except Exception as e:
		print("Exception youtube2 {0}".format(e))
		continue


	print(type(article.topComment))

	try:
		article.topCommentNum = int(WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.uPc.bmd'))).text.strip())
		browser.switch_to.default_content()
		article.tag = 'video'
	except Exception as e:
		print("Exception youtube3 {0}".format(e))
		continue	

	try:
		if len(article.img) > 2 and len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10 and article.topCommentNum > MIN_LIKES:
			rowElements.append(article)
		else:
			print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s article.topCommentNum %s " %( article.title,article.topComment, article.url, article.age, article.topCommentNum)
			pass
	except Exception as e:
		print("Exception: {0}".format(e))

print("processing json")		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
browser.quit()
