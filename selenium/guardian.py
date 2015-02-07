import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import guardian_comment, timeHelper, common_classes, jsonHelper, re, imageUtil
from urlparse import urlparse




class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        ##self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)


    def classifyTag(tag):
        if tag =='commentisfree':
            return 'opinion'
        else:
            return tag


    def test_search_in_python_org(self):
        
        NAME = 'guardian'
        DOMAIN_URL = "http://www.the%s.com/us" % NAME
        containers = None
        articles = []
        MAX_NUM_ARTICLES = 10
        COMMENT_NUM_CRITERIA = 200
        TOP_COMMENT_STRING_LEN = 20
        TOP_COMMENT_NUM = 10
        DEFAULT_TIME = 1416691395
        TIME_WAIT = 2

        pages = []
        #self.driver.implicitly_wait(1)
        print "PID: %s" % self.driver.binary.process.pid
        self.driver.get(DOMAIN_URL)
        headlines = []
        rowElements = []

        try:
            ##WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-item__comment-count")))
            headlines = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fc-item__container')))[0:12]
        except Exception as e:
            print "WARNING: Expected containers: %s" % e
            return

        # for index, subject in enumerate(headlines[:]):
        #     subject_url = subject.get_attribute('href')
        #     if 'video' in subject_url:
        #         print "Skip url: %s" % subject_url
        #         continue
        #     a = common_classes.Article(subject_url)
        #     a.title = subject.find_element_by_xpath("span").text.strip()
        #     a.tag = urlparse(subject_url).path.split('/')[1]
        #     if len(a.title) > 2 and len(a.tag) > 2:
        #         pages.append(a)

        # isFirstPage = True
        # for page in pages[:]:
        #     guardian_comment.findTopCommentAndTopNumber(self, page,isFirstPage,TIME_WAIT ).copy()


        for index, container in enumerate(headlines[:]):

            comment = None
            article = None
            title = None
            href = None
            textTitle = None

            try:
                commentNum = container.find_element_by_css_selector(".js-item__comment-count").text.strip()

                numStr = re.sub(r'\D',"",commentNum)

                #print "numComment %s" % numStr
                numComments = int(numStr)
                if numComments < 50:
                    #print "Continue NumComments %s" % numComments
                    continue
                
                article = container.find_element_by_css_selector(".fc-item__link")
                url = str(article.get_attribute('href')).strip()
                print "URL %s" % url
                if 'video' in url or 'live' in url:
                    print "Skip url: %s" % url
                    continue
                a = common_classes.Article(url)
                a.numComments = numComments

                a.title = article.find_element_by_css_selector(".u-faux-block-link__cta").text.strip()
                #print "Title: %s" % a.title 
                theTag = urlparse(url).path.split('/')[1]
                #print "Tag: %s" % theTag
                
                a.tag = theTag
                
                if len(a.title) > 2 and len(a.tag) > 1:
                    pages.append(a)

            except Exception as e:
                print "WARNING: article %s currentNum %s" % (e, len(pages))


        isFirstPage = True

        for page in pages[:]:

            thePage = guardian_comment.findTopCommentAndTopNumber(self, page ,isFirstPage,TIME_WAIT )
            #isSuccess = imageUtil.imageProcedure(browser, article.title, [common_classes.CSSXPATH(".image img", "src", "css"), common_classes.CSSXPATH("img.media-viewer-candidate", "src", "css")])
            isSuccess = imageUtil.imageProcedure(self.driver, thePage.title, cssXpaths=[common_classes.CSSXPATH("img.maxed.responsive-img", "src", "css"), common_classes.CSSXPATH("video", "poster", "css")])
            #isSuccess = guardian_comment.findImage(self , thePage.title)
            isFirstPage = False
            thePage.img = imageUtil.imageTitlePathJPG(thePage.title)

            if isSuccess and len(thePage.img) > 1 and len(thePage.title) > 2 and thePage.numComments > 5 and len(thePage.url) > 2 and len(thePage.topComment) > 2 and thePage.topCommentNum > 2 and thePage.age > 1 and len(thePage.tag) > 1:
                rowElements.append(thePage)


            print "FINAL###########################################################"
            print "title %s " % thePage.title
            print "numComments %s " % thePage.numComments
            print "url %s " % thePage.url 
            print "topComment %s " % thePage.topComment
            print "topCommentNum %s " % thePage.topCommentNum
            print "age %s " % thePage.age
            print "tag %s " % thePage.tag
            print "img %s " % thePage.img

        print "final 0"
        timeHelper.sortTimeForGuardian(rowElements)

        print "final 1"
        jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
        print "final 2"
        #self.driver.quit()


            # for key, value in topCommentDict.iteritems():
            #     print "Key NOV25 %s Value %s" % (key, value)
            
            #     if 'topComment' == key and isinstance(value, basestring) and len(value) > TOP_COMMENT_STRING_LEN:
            #         x.topComment = value
            #     elif 'topCommentNumber' == key and isinstance(value, int) and value > TOP_COMMENT_NUM:
            #         x.topCommentNum = value
            #     elif 'timeStamp' == key and isinstance(value, int) and value > DEFAULT_TIME:
            #         x.age = value
            #     else:
            #         print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
            #         articles.remove(x)
            #         print ""
            #         break


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()




