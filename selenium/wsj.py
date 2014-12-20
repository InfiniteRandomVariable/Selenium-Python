from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, techCrunchTime, wsj_time, time


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://online.wsj.com'

WEBSITE_URL = '%s/home-page' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 1
MAX_RANKING = 5
MIN_COMMENT_NUM = 100/divider
#MIN_COMMENT_NUM = 1/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140


#first 5
POPULARS = '.headlineSummary.trendingNow .newsItem>li'
#xpath h2/a href and text
# iterate this list and filter out the class element that contain one of these words"subPrev tipTree tooltipType-news"


#num of reviews text
#NUM_REVIEWS = '.fyre-comment-count>span'
NUM_REVIEWS ='.comments_header'

#ID
#grab the first avaiable row
REVIEWS = '.fyre-stream-sort-newest.fyre-stream-sort-selected'
#REVIEWS ='.fyre-stream-sort-options'
#REVIEWS = '#livefyre-comment > div > div > div.fyre-stream-header > div.fyre-stream-sort > div.fyre-stream-sort-options > a.fyre-stream-sort-newest.fyre-stream-sort-selected'
#REVIEWS = './/div[@id="livefyre-comment"]/div/div[1]/div[7]/div[2]/div[1]/a[1]'
REVIEWS1 = 'a.fyre-stream-sort-top-comments'
#REVIEWS1 = '.fyre-stream-sort-top-comments'
REVIEWS_XPATH1 = '//div[@id="livefyre-comment"]/div/div/div[7]/div[2]/div[1]/a[3]'
REVIEW = '.fyre-comment>p'
#REVIEW_X = './/div[@id="livefyre-comment"]/div/div/div[8]/div[1]/article[2]/div[1]/section/div/p'

#Dec. 14, 2014 11:12 p.m. ET
TIME_STAMP ='.timestamp'


TAG = 'popular'

#http://techcrunch.com/2014/12/12/alienware-alpha-review-a-gaming-pc-in-a-tiny-package/#comments


pages=[]
try:
	
	rows = WebDriverWait(browser, 25).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,POPULARS)))[0:MAX_RANKING]


	#print "0"

	rowNum = 1
	#print "SIZE %s" % totalClips

	for row in rows[:]:
		classStr = row.get_attribute('class')
		if 'subPrev' in classStr or 'tipTree' in classStr or 'tooltipType-news' in classStr:
			#print "SKIP %s" % classStr
			continue

		##URL and TITLE
		elm = row.find_element_by_xpath('h2/a')
		_url = elm.get_attribute('href')
		a = common_classes.Article(_url)
		a.title = elm.text.strip()
		#print "TITLE %s" % a.title

		pages.append(a)	

except Exception as e:
	print "Exception: failure in WSJ \n%s" % e


for article in pages[:]:

	
	#print "6"
	url = "%s%s" % (article.url, '#livefyre-comment')
	
	browser.get(url)
	time.sleep(5)
	numCommentsElm = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NUM_REVIEWS)))

	numComments = numCommentsElm.text.strip()

	article.numComments = int(re.search( r'(\d+)\s', numComments).group().strip())

	if article.numComments < MIN_COMMENT_NUM:
		#print "CONTINUE: %s " % article.numComments
		continue

	#"clickHandler: function (self, $el)"
          
	timeStr = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, TIME_STAMP))).text.strip()

	article.age = wsj_time.timeToTimeStamp(timeStr)
	
	article.topComment = WebDriverWait(browser, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, REVIEW))).text.strip()[0:WORDS_LIMIT]
	if len (article.topComment) > (WORDS_LIMIT -1):
		article.topComment = "%s..." % article.topComment

	article.topCommentNum = 0
	article.tag = TAG


	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10:
		rowElements.append(article)
	else:
		#print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( article.title,article.topComment, article.url, article.age)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"wsj")
browser.quit()
