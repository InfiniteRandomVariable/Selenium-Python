from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper


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

browser.get('http://www.billboard.com/charts/hot-100')

#find the first 15 rows
rowElements = []

# allow top 5 items to be in the listing
MIN_RANKING = 4

try:
	rowElements = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".row-primary")))[:15]
except Exception as e:
	print "Exception: failure in ROW ELEMENTS"
	browser.quit()
	sys.exit()
	

if len(rowElements) < 5:
	print "ROW ELEMENT COUNT %s < 5 " % len(rowElements)
	browser.quit()
	sys.exit()

articles = []


for row in rowElements[:]:

	videoElement = None
	try:
		videoElement = row.find_element_by_css_selector('.row-watch>a')
	except Exception as e:
		print "Exception: failure in VIDEO ELEMENT"
		continue

	hf = videoElement.get_attribute("href")
	if hf == None:
		print "Can't find the video element"
		continue

	print "HREF: %s" % hf
	a = common_classes.Article(hf)
	a.age = 100

	rank = row.find_element_by_css_selector('.this-week')


	a.topCommentNum = 0

	try:
		a.age = int(rank.text.strip())
	except Exception as e:
		print "Exception in converting to age number: %s\n%s" % (a.age, e)
		continue

	a.numComments = 0

	mostStreamItem = False

	try:
		row.find_element_by_css_selector('.fa.fa-star')
		mostStreamItem = True
	except Exception:
		print "Fail to meet condition\nAGE:%s" % a.age
		pass

	if a.age > MIN_RANKING and mostStreamItem == False:
		print "Fail to meet condition\nAGE:%s" % a.age
		continue


	#song title
	title = row.find_element_by_css_selector('.row-title>h2').text.strip()
	#artist name
	a.topComment = row.find_element_by_css_selector('.row-title>h3>a').text.strip()


	if mostStreamItem:
		a.title = "Streaming Gainer and Rank: %s\n%s" % (a.age, title)
	else:
		a.title = "Hot-100: %s\n%s" % (a.age, title)

	a.tag = "video"

	print "SONG MESSAGE:\n%s\nArtist:%s" %(a.title, a.topComment)
	articles.append(a)


jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),articles,"billboard")
browser.quit()


