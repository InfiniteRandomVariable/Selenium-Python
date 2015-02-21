from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re, time, articleUtil, imageUtil


##PROBLEM
## only can find the first 4 items. Maybe memory problem?

browser = webdriver.Firefox()

BASE= 'http://www.amazon.com'

WEBSITE_URL = '%s/gp/new-releases/books/ref=zg_bs_tab_t_bsnr' % BASE

browser.get(WEBSITE_URL)

rowElements = []
divider = 1
MAX_RANKING = 4
MIN_COMMENT_NUM = 80/divider
MAX_PAGE_VISIT = 4

TOP_SELLERS = '.zg_itemImmersion'

#href and book title
BOOK_DETAILS = '.zg_title>a'
AUTHOR = '.zg_byline'

#num of reviews text
NUM_REVIEW = '.crAvgStars>a'

#ID
#grab the first avaiable row
REVIEWS = '#productReviews>tbody>tr>td>div'



LIKES = '.a-size-small.a-color-secondary'

#Text
REVIEW_TITLE = '.a-size-base.a-text-bold'
#Text first 150 words
REVIEW_TEXT ='.MHRHead'
TAG = 'ranking'
WAIT_SECONDS = 2
#WORD_LIMIT = 160

#http://techcrunch.com/2014/12/12/alienware-alpha-review-a-gaming-pc-in-a-tiny-package/#comments


books=[]
try:
	
	rows = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,TOP_SELLERS)))[0:MAX_RANKING]


	#print "0"

	rowNum = 1
	#print "SIZE %s" % totalClips

	for row in rows[:]:
	
		
		##URL and TITLE
		try:
			elm = WebDriverWait(row, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,BOOK_DETAILS )))

			bookURL = elm.get_attribute('href')
			book = common_classes.Article(bookURL)

			numReviewElm = WebDriverWait(row, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,NUM_REVIEW )))
			
			book.numComments = int(re.sub(r'[^\d]', '', numReviewElm.text))

			book.tag = numReviewElm.get_attribute('href').strip()

			author = row.find_element_by_css_selector(AUTHOR).text.strip()
			book.title = "Book Release: %s %s" % (elm.text.strip(), author) 

			print("TITLE: {0} Comment: {1}".format(book.title, book.numComments))
			rowNum = rowNum + 1
			if book.numComments > MIN_COMMENT_NUM:
				books.append(book)
		except Exception as theE:
			print "Exception: failure in amz0 %s" % theE

except Exception as e:
	print "Exception: failure in amz1 %s" % e


isFirstPage = True

for book in books[:]:

	try:
		#print "6"
		print("find new book")
		browser.get(book.url)
		time.sleep(WAIT_SECONDS)

		print("find new book 1")
		reviewSectionElm = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,"revMHRL")))
		if not reviewSectionElm:
			continue
		print("find new book 2")

		commentElm = reviewSectionElm.find_element_by_css_selector(".MHRHead")
		print("find new book 3")
		if not commentElm:
			continue

		print("find new book 4")
		comment = re.sub(r'\<br\/\>*', '', commentElm.text)

		if not comment or len(comment) < 2:
			print("Error comment {0}".format(comment))
			continue

		print("find new book 5")
		titleElm = reviewSectionElm.find_element_by_css_selector(".a-size-base.a-text-bold")
		if not titleElm:
			continue

		title = re.sub(r'\\\"', '"', titleElm.text)
		if not title or len(title) < 2:
			print("Error title {0}".format(title))
			continue


		## #revMHRL .MHRHead
		## select the comment
		## delete all the <br/>

		## #revMHRL .a-size-base.a-text-bold
		## select title


		#download the image

		print("find new book 6")

		WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#imgThumbs .a-color-link'))).click()
		#igImage

		print("about to call getImageAndSave")
		isSuccess = imageUtil.imageProcedure(browser, book.title, [common_classes.CSSXPATH("#igImage", "src", "css")])
		print("return from getImageAndSave")        
		book.img = imageUtil.imageTitlePathJPG(book.title)





		tComSize = len(title)
		rTextSize = len(comment)
		##if(len(reviewText) > 98):
		print("make title 0")
		if tComSize > 3 and rTextSize > 3:	
			book.topComment = "{0} - {1}".format(title, comment)
		elif tComSize > 3:
			book.topComment = title
		elif rTextSize > 3:
			book.topComment = comment
		print("make title 1")
		book.topComment = articleUtil.truncatedStringForRow(book.topComment);

		book.tag = TAG

		book.age = 10000

		print("make title 2")
		if isSuccess and len(book.img) > 1 and len(book.title) > 2 and len(book.topComment) > 3 and len(book.url) > len(BASE) and book.numComments > MIN_COMMENT_NUM and book.age > 10:
			rowElements.append(book)

	except Exception, e:
		print "Exception3: failure in techcrunch1 \n%s" % e


			
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,"amzbooks", 1)
browser.quit()

