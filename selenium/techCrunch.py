from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, techCrunchTime,time, articleUtil


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

##grab the links


browser = webdriver.Firefox()
NAME = "techcrunch"
BASE= 'http://%s.com' % NAME

WEBSITE_URL = '%s/popular' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 10
MAX_RANKING = 5
MIN_COMMENT_NUM = 80/divider
MAX_PAGE_VISIT = 4
MIN_LIKES = 20/divider

FIRST_SECTION = ".lc.flush"

ROWS = '.block-content'
ROM_TIME = '.timestamp'
TAG = 'tech'
WAIT_SECONDS = 2

#http://techcrunch.com/2014/12/12/alienware-alpha-review-a-gaming-pc-in-a-tiny-package/#comments


pages=[]
try:
	
	rows = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,ROWS)))


	#print "0"

	rowNum = -1
	#print "SIZE %s" % totalClips

	for row in rows[:]:
	
		
		##URL and TITLE
		commentCount = 0
		try:
			commentCount = int(WebDriverWait(row, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".fb_comments_count"))).text.strip())
		except Exception as ie:
			print "Exception: failure in techcrunch0.0 \n%s" % ie
		# commentCount = int(row.find_element_by_css_selector(".fb_comments_count").text.strip())

		rowNum = rowNum + 1
		if commentCount > MIN_COMMENT_NUM and len(pages) < MAX_PAGE_VISIT:
			#print "2 commentCount %s" % commentCount
			clipElm = ''
			try:
				clipElm = row.find_element_by_xpath("//a[@data-omni-sm='gbl_river_headline,%s']" % rowNum)
			#print "3"
				a = common_classes.Article(clipElm.get_attribute("href").strip())
			#print "4"
				timeStamp = row.find_element_by_css_selector(".timestamp").get_attribute("datetime").strip()
			#print "5"
			#eg. timestamp 2014-12-14 11:05:12
				a.age = techCrunchTime.timeToTimeStamp(timeStamp)
				a.numComments = commentCount
				pages.append(a)
			except Exception as iie:
				print "Exception: failure in techcrunch0.1 \n%s" % iie


except Exception as e:
	print "Exception: failure in techcrunch0 \n%s" % e


isFirstPage = True

for page in pages[:MAX_PAGE_VISIT]:

	try:
		#print "6"
		browser.get(page.url)
		if isFirstPage == False:
			time.sleep(WAIT_SECONDS)
		isFirstPage = False		
		#print "7"
		page.title = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".alpha.tweet-title"))).text.strip()
		print "8"
		#.fb_iframe_widget.fb_iframe_widget_fluid
		#fbElm = WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,".fb_iframe_widget.fb_iframe_widget_fluid")))

		fbFrame = WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,".fb_ltr")))
		#print "8.1"
		browser.switch_to.frame(fbFrame)
		#print "8.2"
		post = WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,".postContainer.fsl.fwb.fcb")))
		#print "9"
		commentLikeNum = int(post.find_element_by_css_selector(".text").text.strip())
		print "10 Numlikes %s " % commentLikeNum

		if commentLikeNum > MIN_LIKES:
			print "10.1"
			page.topComment = post.find_element_by_css_selector(".postText").text
			page.topComment = articleUtil.truncatedStringForRow(page.topComment)
			print "11 comment: %s" % page.topComment
			page.tag = TAG
			page.topCommentNum = commentLikeNum

			if len(page.title) > 2 and len(page.topComment) > 2 and len(page.url) > len(WEBSITE_URL) and page.age > 100000:
				#print "12"
				rowElements.append(page)
			else:
				print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s " %( page.title, page.topComment, page.url, page.age)	
				pass
					
		browser.switch_to.default_content();

	except Exception, e:
		browser.switch_to.default_content();
		print "Exception: failure in techcrunch1 \n%s" % e


			##.postContainer.fsl.fwb.fcb
			#CSS_SELECTOR after the page is being loaded ".postContainer.fsl.fwb.fcb"
#print "13"			
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements[0:2],NAME, 1)
browser.quit()

