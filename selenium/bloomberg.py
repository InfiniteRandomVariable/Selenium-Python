from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time, disqus, disqus_time, articleUtil


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

NAME='bloomberg' 
BASE= 'http://www.%s.com' % NAME 

WEBSITE_URL = '%s/popular/' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 3
MIN_LIKES = 30/divider
MIN_COMMENT_NUM = 100/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=5
WAIT_SECONDS = 3

POPULARS = '.thumbnail_container'


	##.thumbnail_container
	##.small_img and attribute 'alt' !== 'Dynamic'


	#xpath //img[@alt='Dynamic']  skip
	#or
	#without img tag

pages=[]
try:
	
	rows = WebDriverWait(browser, 25).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,POPULARS)))[0:MAX_RANKING]

	for row in rows[:]:

		
		rowElm = row.find_element_by_css_selector('.small_img')
		print "2"
		attribute = rowElm.get_attribute('alt')
		# cannot contain dynamic coz the associated article doesn't contain comments
		print "3"
		attriLen = len(str(attribute).strip())
		if 'Dynamic' in attribute or attriLen < 2:
			print "Attribute: %s :%s :%s" % (attribute, len(str(attribute))>0, len(str(attribute)))
			continue
		url = "%s" % row.find_element_by_xpath('a').get_attribute('href')
		a = common_classes.Article(url.strip())
		if len(a.url) > 5:
			pages.append(a)

		print "URL %s" % a.url

except Exception as e:
	print "Exception: failure in bloomberg \n%s" % e

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
		article.title = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.article_title'))).text.strip()
		#epoch 					1419205695000
		#standardUTC			1418990429

		article.age  = int(WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".date"))).get_attribute('epoch'))/1000
		#theTimeStampText = theTimeStampTextElm.get_attribute('epoch')
		#article.age = int(theTimeStampText)/1000
		if article.age == None or article.title == None or article.age < 10 or len(article.title) < 2:
			print "timestamp length %s\n title:%s " % (article.age, article.title)
			continue
		print "timeStamp: %s" % article.age
	except Exception as e:
		print "EXCEPTION Time %s " % e
		continue

	disqus.findTopCommentAndTopNumber(browser, article,MIN_COMMENT_NUM,MIN_LIKES)
	article.tag = 'news'



	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10:
		rowElements.append(article)
	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( article.title,article.topComment, article.url, article.age)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
browser.quit()
