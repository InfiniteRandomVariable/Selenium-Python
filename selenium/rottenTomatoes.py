from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, imageUtil, time


browser = webdriver.Firefox()

NAME='rottentomatoes'
SHORT_NAME = 'rtomatoes'
WEBSITE_URL ='http://www.%s.com' % NAME

browser.get(WEBSITE_URL)

#find the first 15 rows
rowElements = []
# allow top 5 items to be in the listing
MIN_RANKING = 4
MIN_SCORE = 74
MAX_RANKING_TOP_BOX_OFFICE = 5

OPENING_THIS_WEEK = "Opening"
BOX_OFFICE = "Top-Box-Office"
WAIT_SECONDS = 3

#"Top-Box-Office"
#MIN_SCORE = 74

try:

	for sectionId in [OPENING_THIS_WEEK,BOX_OFFICE]:

		primeRowElements = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,sectionId)))

		movies = None

		isOpenningThisWeek = True
		if sectionId == OPENING_THIS_WEEK:
			movies = primeRowElements.find_elements_by_css_selector(".sidebarInTheaterOpening")

		elif sectionId == BOX_OFFICE:
			#continue

			isOpenningThisWeek = False
			movies = []

			for index in range(1,MAX_RANKING_TOP_BOX_OFFICE):
				movies.append(primeRowElements.find_element_by_xpath("tbody/tr[%s]" % index))

		for movie in movies[:]:
			intScore = 0
			try:
				scoreText = movie.find_element_by_css_selector(".tMeterScore")
				score = re.sub(r'%$', "",scoreText.text.strip())
				intScore = int(score)
			except Exception as e:
				print("Exception: {0}".format(e))
				continue

			if intScore > MIN_SCORE and isOpenningThisWeek == True or isOpenningThisWeek == False:
				

				titleElm = movie.find_element_by_css_selector(".middle_col>a")
				title = titleElm.text.strip()
				url = titleElm.get_attribute("href")

				print "4 title: %s url: %s" % (title, url)
				if len(title) > 0 and len (url) > 2:

					a = common_classes.Article(url)

					if isOpenningThisWeek == True:
						a.title = "Movie This Week: %s" % title
					elif isOpenningThisWeek == False:
						revenue = movie.find_element_by_css_selector(".right_col.right").text.strip()
						a.title = "Box Office: %s - %s" % (title, revenue)
					a.topComment = '{:}%'.format(intScore)
					a.tag = 'ranking'
					a.age = 0
					a.topCommentNum = intScore
					print "RESULT title:%s\n topComment:%s tag:%s topCommentNum:%s" % (a.title, a.topComment, a.tag, a.topCommentNum)
					rowElements.append(a)


except Exception as e:
	print "Exception: failure in homepage-opening-this-week\n%s" % e


for a in rowElements[:]:
	browser.get(a.url)
	time.sleep(WAIT_SECONDS)
	isSuccess = imageUtil.imageProcedure(browser, a.title , cssXpaths=[common_classes.CSSXPATH("#poster_link>img", "src", "css")])
	a.img = imageUtil.imageTitlePathJPG(a.title)
	if not len (a.img) > 2 or isSuccess:
		rowElements.remove(a)


timeStamp = timeHelper.APP_TIMESTAMP()
jsonHelper.writeToFile(timeStamp,rowElements,SHORT_NAME)
browser.quit()


