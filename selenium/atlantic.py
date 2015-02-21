import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import atlantic_comment, timeHelper, common_classes
from urlparse import urlparse
import json, jsonHelper, imageUtil, articleUtil



class FrontAtlantic(unittest.TestCase):

    def setUp(self):
        ##self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)


    def classifyTag(tag):
        if tag =='commentisfree':
            return 'opinion'
        else:
            return tag


    def test_search_in_python_org(self):
        
        
        DOMAIN_URL = "http://www.theatlantic.com"
        containers = None
        articles = []
        TOP_COMMENT_STRING_LEN = 20
        ##CHANGE
        ##TOP_COMMENT_NUM = 10
        TOP_COMMENT_NUM = 2
        DEFAULT_TIME = 141627
        TITLE_CRITERIA = 5
        ##CHANGE
        ##NUM_COMMENTS_CRITERIA = 10
        NUM_COMMENTS_CRITERIA = 2
        TIME_WAIT = 2

        #self.driver.implicitly_wait(100)
        self.driver.get(DOMAIN_URL)

        keyElements = ["//a[@data-tb-region-item='Carousel1']","//a[@data-tb-region-item='Carousel2']","//a[@data-tb-region-item='Carousel3']","//a[@data-tb-region-item='Carousel4']"]
        #keyElements = ["//a[@data-tb-region-item='Carousel1']","//a[@data-tb-region-item='Carousel3']"]

        for keyElement in keyElements[:]:

            try:
                elem = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,keyElement)))
                hf = elem.get_attribute("href")
               # print 'HREF: %s' % hf
                if len(hf) > 8:
                    articles.append(common_classes.Article(hf))

            except TimeoutException:
               # print "WARNING: TimeoutException containers"
                continue
            except NoSuchElementException:
               # print "WARNING: No NoSuchElementException containers"
                continue
            except Exception as e:
               # print "WARNING: Expected containers: {}".format(e)
                continue


        articleLen = len(articles)
        isFirstPage = True
        for x in articles[:]:

            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("SEARCH URL: {0}".format(x.url))


            topCommentDict = atlantic_comment.findTopCommentAndTopNumber(self, x.url, isFirstPage,TIME_WAIT)
            isFirstPage = False



            if isinstance (topCommentDict,dict) == False or isinstance (topCommentDict,dict) and len(topCommentDict) == 0:
                #print "REMOVED TITLE %s" % x.title
                articles.remove(x)
                #print ""
                continue
#cssXpaths=[common_classes.CSSXPATH(".row-image", "style", "css")] , webElement=imageElm)

            #isSuccess = guardian_comment.findImage(self , thePage.title)
            isFirstPage = False
            


            x.tag = urlparse(x.url).path.split('/')[1]
            if x.tag in "entertain":
                x.tag = "enews"
           # print 'TAG: %s URL: %s' % (x.tag, x.url)

            for key, value in topCommentDict.iteritems():
               # print "Key NOV25 %s Value %s" % (key, value)
            
                if 'topComment' == key and isinstance(value, basestring) and len(value) > TOP_COMMENT_STRING_LEN:
                    x.topComment = value
                elif 'topCommentNumber' == key and isinstance(value, int) and value > TOP_COMMENT_NUM:
                    x.topCommentNum = value
                elif 'timeStamp' == key and isinstance(value, int) and value > DEFAULT_TIME:
                    x.age = value
                elif 'title' == key and isinstance(value, basestring) and len(value) > TITLE_CRITERIA:
                    x.title = value
                    ##change this ugly code

                    imageUtil.imageProcedure(self.driver, x.title , cssXpaths=[common_classes.CSSXPATH(".photo>img", "src", "css"), common_classes.CSSXPATH("article.article style", "get_text", "css")])
                    x.img = imageUtil.imageTitlePathJPG(x.title)
                elif 'numComments' == key and isinstance(value, int) and value > NUM_COMMENTS_CRITERIA:
                    x.numComments = value                  
                else:
                    print("REMOVED TITLE {0}, url: {1}".format(x.title, x.url))
                  #  articles.remove(x)
                    
                   # break

        timeHelper.sortTimeForAtlantic(articles)
        print("BEFORE Total articles: {0} AFTER Total articles: {1}".format(articleLen, len(articles)))

        fArticles = []

        for article in articles[:]:
            if articleUtil.checkArticle(article):
                fArticles.append(article)

            articleUtil.printArticle(article)


        jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),fArticles,"atlantic")

        # for x in articles[:]:
        #     print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        #     print x.title
        #     print x.numComments
        #     print x.url
        #     print x.topComment
        #     print x.topCommentNum
        #     print x.age
        #     print x.tag
        #     print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()




