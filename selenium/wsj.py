from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, wsj_time, time, articleUtil, imageUtil


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://online.wsj.com'

WEBSITE_URL = '%s/home-page' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 10
MAX_RANKING = 5
MIN_COMMENT_NUM = 50/divider
#MIN_COMMENT_NUM = 1/divider
MAX_PAGE_VISIT = 5
WORDS_LIMIT = 140
WAIT_SECONDS = 5


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
REVIEW_Level1 = '.fyre-comment>p>p'
#REVIEW_X = './/div[@id="livefyre-comment"]/div/div/div[8]/div[1]/article[2]/div[1]/section/div/p'

#Dec. 14, 2014 11:12 p.m. ET
TIME_STAMP ='.timestamp'


TAG = 'popular'
##locate the image from the home page. and download the mobile app and locate the mobile oriented image.

pages=[]
try:
	
	rows = WebDriverWait(browser, 25).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,POPULARS)))[0:MAX_RANKING]


	#print "0"
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
	print "Exception: failure in WSJ1 \n%s" % e

isFirstPage = True

for article in pages[:]:

	
	#print "6"
	url = "%s%s" % (article.url, '#livefyre-comment')
	
	browser.get(url)
	#if isFirstPage == False:
	time.sleep(WAIT_SECONDS * 2)
	#isFirstPage = False


	try:
		numComments = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, NUM_REVIEWS))).text.strip()
		article.numComments = int(re.search( r'(\d+)\s', numComments).group().strip())
		print "numComments %s " % article.numComments
		
		if article.numComments < MIN_COMMENT_NUM:
			print "CONTINUE: %s " % article.numComments
			continue
	except Exception as e:
		print('Exception WSJ2 {0}'.format(e))
		continue



	#"clickHandler: function (self, $el)"
	comment = ''

	try:  
		timeStr = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, TIME_STAMP))).text.strip()

		print 'timeStr %s' % timeStr

		WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.fyre-stream-sort-newest.fyre-stream-sort-selected'))).click()
		time.sleep(WAIT_SECONDS)
		WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.fyre-stream-sort-top-comments'))).click()
		time.sleep(WAIT_SECONDS)
		article.age = wsj_time.timeToTimeStamp(timeStr)

		print 'article.age %s ' % article.age

		try:
			container = WebDriverWait(browser, 250).until(EC.presence_of_element_located((By.CSS_SELECTOR, REVIEW)))

			if container:
				print("container")
				htmlElm = container.get_attribute('innerHTML')
				#print("container: {0}".format(htmlElm))
				article.topComment = container.text

			if not htmlElm:
				container = WebDriverWait(browser, 250).until(EC.presence_of_element_located((By.CSS_SELECTOR, REVIEW)))
				print("container1 ")
				htmlElm = container.get_attribute('innerHTML')
				#print("container1: {0}".format(htmlElm))
				article.topComment = container.text

			print 'article.topComment %s ' % article.topComment

		except Exception as eeee:
			print "Exception WSJ3.01 %s" % eeee

		if len(article.topComment) < 1 and container:
			try:
				print 'article.topComment 1 {0} {1}'.format(article.topComment, article.title)
				newReview = '{0}{1}'.format(REVIEW, 'p')
				elem  = container.find_element_by_css_selector('p')
				print 'article.topComment 1 {0} {1}'.format(article.topComment, article.title)
			except Exception as ee:
				print "Exception WSJ3.1 %s" % ee

			# if len(article.topComment) < 1:
			# 	try:
			# 		print 'article.topComment 2 %s ' % article.topComment
			# 		newReview = '{0}{1}'.format(newReview, '>p')
			# 		article.topComment = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, newReview))).text
			# 		print 'article.topComment 2 %s ' % article.topComment
			# 	except Exception as eee:
			# 		print "Exception WSJ3.2 %s" % eee

		##print('TopComment: {0}'.format(article.topComment))

	except Exception as e:
		print "Exception WSJ3 %s" % e
		continue


	article.topComment = articleUtil.truncatedStringForRow(article.topComment)
	# if len (article.topComment) > (WORDS_LIMIT -1):
	# 	article.topComment = "%s..." % article.topComment

	article.topCommentNum = 0
	article.tag = TAG

	print("about to call getImageAndSave")
	isSuccess = imageUtil.imageProcedure(browser, article.title, [common_classes.CSSXPATH(".vidThumb", "style", "css"), common_classes.CSSXPATH(".image-container img", "src", "css"), common_classes.CSSXPATH(".wsj-slideshow-image", "data-in-large-data-lazy", "css")])
	print("return from getImageAndSave")        
	article.img = imageUtil.imageTitlePathJPG(article.title)	


	if isSuccess and len(article.img) > 1 and len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10:
		print('added: {0}'.format(article.title))
		rowElements.append(article)
	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( article.title,article.topComment, article.url, article.age)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"wsj",1)
browser.quit()
