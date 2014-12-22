from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time, disqus, disqus_time


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://www.wired.com'

WEBSITE_URL = '%s' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 1
MIN_LIKES = 10/divider
MIN_COMMENT_NUM = 15/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=3
WAIT_SECONDS = 3

POPULARS = '.row1 .headline>h2 .module-homepage'


pages=[]
try:
	
	rows = WebDriverWait(browser, 25).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,POPULARS)))[0:MAX_RANKING]

	for row in rows[:]:
		_url = row.get_attribute('href')
		a = common_classes.Article(_url)
		a.title = row.text.strip()
		print "TITLE %s" % a.title
		if len(a.url) > 5 and len(a.title) > 3:
			pages.append(a)	
except Exception as e:
	print "Exception: failure in WSJ \n%s" % e

isFirstPage = True
for article in pages[:]:
	#print "6"
	
	browser.get(article.url)
	if isFirstPage == False:
		time.sleep(WAIT_SECONDS)
	isFirstPage = False

	article.tag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".blogName>a"))).text.strip()
	
	try:
		_time = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH,"//time")))
		article.age = disqus_time.timeToTimeStamp(_time.get_attribute("datetime"))
		print "timeStamp: %s" % article.age
	except Exception as e:
		print "EXCEPTION Time %s " % e
		continue

	disqus.findTopCommentAndTopNumber(browser, article,MIN_COMMENT_NUM,MIN_LIKES)



	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10:
		rowElements.append(article)
	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( article.title,article.topComment, article.url, article.age)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"wired")
browser.quit()
