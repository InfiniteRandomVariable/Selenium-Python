from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://www.hulu.com'

WEBSITE_URL = '%s/browse/picks/trending-now' % BASE

browser.get(WEBSITE_URL)

rowElements = []
MAX_RANKING = 5

FIRST_SECTION = ".subgrid"


try:
	
	grid = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,FIRST_SECTION)))
	clips = grid.find_elements_by_css_selector(".item")[0:MAX_RANKING]
	

	totalClips = len(clips)
	counter = totalClips
	#print "SIZE %s" % totalClips

	for clip in clips[:]:
	
		rowNum = totalClips - counter 
		clipElm = clip.find_element_by_xpath("//a[@data-model-position='%s']" % rowNum)
	
		
		#http://www.hulu.com/watch/726517?playlist_id=1031
		#replace the ?playlist_id=1031 with regex
		a = common_classes.Article(re.sub(r'\?.+$', "",clipElm.get_attribute("href").strip()))
	
		a.title = clip.find_element_by_css_selector(".headline").text.strip()
		source = clip.find_element_by_css_selector(".source").text.strip()
		duration = clip.find_element_by_css_selector(".duration").text.strip()

		a.topComment = '%s%s' % (source , duration)
		a.tag = 'video'
		a.age = 0
		a.topCommentNum = counter
		counter = counter - 1

		if len(a.title) > 2 and len(source) > 2 and len(duration) > 1 and len(a.url) > len(BASE):
			rowElements.append(a)			

except Exception as e:
	print "Exception: failure in hulu \n%s" % e


jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"hulu")
browser.quit()