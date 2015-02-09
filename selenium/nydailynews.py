from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, nydailynews_time, time, articleUtil, imageUtil


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://www.nydailynews.com'

WEBSITE_URL = '%s/news' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 1
MIN_LIKES = 10/divider
MIN_COMMENT_NUM = 15/divider
MIN_ARTICLES = 1
#MIN_COMMENT_NUM = 1/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=3
WAIT_SECONDS = 3


#first 5
POPULARS = '.mostPopularTabs>ol>li>a'
#xpath h2/a href and text
# iterate this list and filter out the class element that contain one of these words"subPrev tipTree tooltipType-news"


#num of reviews text
NUM_REVIEWS = '.goto-comments'
NUM_LIKES ='.gig-comment-vote-pos.gig-comment-vote-with-value'

#ID
#grab the first avaiable row
REVIEW = '.gig-comment-body'
TIME_STAMP ='#a-date-published'

#get the list
#.mostPopularTabs>ol>li
#get the first 4 items
#create an article and grep title and url


#visit every page
#wait two seconds
#.gig-comment-vote-pos.gig-comment-vote-with-value
#if more than MIN_Likes
	#.gig-comment-body get first 140 characters
	#.a-date-published 2014-12-20T19:11:26
		#get attribute content for time variable
		#convert time
		#assign to article obj
#else: continue 



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

	numCommentsText = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, NUM_REVIEWS))).text.strip()



	##article .a-image img src
	#article .ndn_startOverlayContainer.ndn_playerOverlay .backstretch>img src

	nCT = re.sub(r'\D',"",numCommentsText)

	try:
		article.numComments = int(nCT)
	except Exception as e:
		print "CONTINE 1: %s" % article.numComments
		continue

	if article.numComments < MIN_COMMENT_NUM:
		print "CONTINUE2: %s " % article.numComments
		continue

	#"clickHandler: function (self, $el)"
	numLikesText = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, NUM_LIKES))).text.strip()
	print "numliketext: %s" % numLikesText

	tCN = re.sub(r'\D',"",numLikesText)

	try:
		article.topCommentNum = int(tCN)
	except Exception as e:
		print "CONTINUE 3: %s" % article.topCommentNum
		continue

	if article.topCommentNum < MIN_LIKES:
		print "CONTINUE4: %s " % article.topCommentNum
		continue



	timeStr = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, TIME_STAMP))).get_attribute('content').strip()

	article.age = nydailynews_time.timeToTimeStamp(timeStr)
	article.topComment = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, REVIEW))).text
	article.topComment = articleUtil.truncatedStringForRow(article.topComment)
	#if len (article.topComment) > (WORDS_LIMIT -1):
	#	article.topComment = "%s..." % article.topComment

	firstURL = re.sub(r'/+[^\/]+$',"", article.url)
	finalReg = r'^%s/' % WEBSITE_URL
	article.tag = re.sub(finalReg,"", firstURL)
	print "FINAL URL %s" % article.tag


	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10:

		isSuccess = imageUtil.imageProcedure(browser, article.title, cssXpaths=[common_classes.CSSXPATH("article .a-image img", "src", "css"), common_classes.CSSXPATH("article .ndn_startOverlayContainer.ndn_playerOverlay .backstretch>img", "src", "css")])
		article.img = imageUtil.imageTitlePathJPG(article.title)
		if isSuccess and len(article.img) > 2:
			rowElements.append(article)

	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( article.title,article.topComment, article.url, article.age)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"nydailynews",MIN_ARTICLES)
browser.quit()
