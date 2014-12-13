from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper, time, re


#find chart highlights
#.fa.fa-star
#.fa-ul.row-awards li text matching to 'Biggest gain in streams'
#
#
#
#find top 3 songs 
#.row-primary
#	.fa.fa-li.fa-signal(one search) or .fa-ul.row-awards>li (more than 5 search and require string match for each)
#	find chart highlights && Biggest gain in streams
#
#	.row-watch>a
#	if it has no video, delete it
#	capture the video URL
#	
#	.this-week
#	rank
#	.row-title>h2
#	song title
#
#	.row-title>h3>a
#	singer name

browser = webdriver.Firefox()

browser.get('http://www.people.com/people/news/')

#find the first 15 rows
rowElements = []

# allow top 5 items to be in the listing
MIN_RANKING = 4
MIN_COMMENT = 25
COMMENT_NUM_CRITERIA = 200

popular = None

try:
	popular = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,"most-shared")))
except Exception:
	print "Exception: most shared"
	browser.quit()
	sys.exit()

try:
	rowElements = popular.find_elements_by_css_selector('.text>h4>a')[:4]
	#rowElements = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".text>h4>a")))[:5]
except Exception as e:
	print "Exception: failure in ROW ELEMENTS"
	browser.quit()
	sys.exit()
	

articles = []
rows = []

for row in rowElements[:]:
	
	a = common_classes.Article(row.get_attribute("href"))
	a.title = row.text.strip()
	if len(a.url) > 2 and len(a.title) > 2:
		rows.append(a)

for index in range(len(rows)):

	print "BEGINNING TO SEARCH"
	# href = row.get_attribute("href")
	# title = row.text
	# print "TITLE: %s HREF: %s" % (title, href)

	# if len(href) < 5 or len(title) < 3:
	# 	print "CONTINUE\nTitle: %s\nHref: %s" % (title, href)
	# 	continue
	a = rows[index]
	browser.get(a.url)
	

	try:
		frame = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"iframe#dsq-2")))
		browser.switch_to.frame(frame)

	except Exception:
		print "#################### EXCEPTION fail to switch iframe"
		continue

	try:
		##xpath
        ##//a[@data-nav="conversation"]
        ##".dropdown-toggle"
		WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-nav='conversation'][@data-toggle='dropdown']"))).click()
	except Exception:
		print "############# EXCEPTION //a[@data-nav='conversation']"
		browser.switch_to.default_content();
		continue

	try:
		WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-sort='popular']"))).click()
	except Exception as e:
		print "################### EXCEPTION a[@data-sort='popular']"
		browser.switch_to.default_content();
		continue

    ##a data-role="username"





	print "TIME SLEEP"

	time.sleep(5)

	topCommentNumber = 0

	try:
		text = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".updatable.count"))).text

		if isinstance(text, basestring) and len(text) > 0:
			try:
				topCommentNumber = int(text)
			except Exception as e:

				print "############# EXCEPTION fail to convert ot number"

	except Exception as e:
		print "#######################EXCEPTION Comment Number"
    	
	if topCommentNumber < MIN_COMMENT:
		print "CONTINUE: can't meet top comment number requirement %s < %s" % (topCommentNumber, MIN_COMMENT)
		browser.switch_to.default_content();
		continue

	comNum = 0
    ##.comment-count

	try:
		text = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment-count"))).text

		print "Time Text %s" % text

		if isinstance(text, basestring) and len(text) > 0:

			numText = re.search( r'^\d+\S', text)

			print "numText: %s" % numText.group()
			try:

				comNum = int(numText.group())

			except Exception:
				print "**************EXCEPTION comment Number"

	except Exception as e:
		print "############################# EXCEPTION comment count %s" % e

	if comNum < COMMENT_NUM_CRITERIA:
		print "CONTINUE: can't meet the comment number requirement %s < %s" % (comNum, COMMENT_NUM_CRITERIA)
		browser.switch_to.default_content();
		continue

	topComment = ''

	try:
		firstComment = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".post-message")))
		elms = firstComment.find_elements_by_css_selector('p')

		for elm in elms[:]:
			topComment = topComment + ' ' + elm.text

	except Exception as e:
		print "NoSuchElementException /TimeoutException .content__dateline>time"
		browser.switch_to.default_content();
		continue

	topComment = re.sub(r'\\', "",topComment.strip())

	if len (topComment) > 10:
		print "top comment"
		
		a.numComments = comNum
		a.topComment = topComment
		a.age = 0
		a.topCommentNum = topCommentNumber
		a.tag = 'entertainment'
	
	articles.append(a)
	#browser.switch_to.default_content();

jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),articles,"people")
browser.quit()

