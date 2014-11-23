import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import guardian_comment



class Article:
   
    def __init__(self, url, title, numComments):
        self.url = url
        self.title = title
        self.numComments = numComments
        self.topComment = ''
        self.topCommentNum = 0
      
   
    def url(self):
        return self.url
    def title(self):
        return self.title
    def numComments(self):
        return self.numComments
    def setTopComment(self, comment):
        self.topComment = comment
    def setTopCommentNum(self, num):
        self.topCommentNum = num
    def topComment(self):
        return self.topComment
    def topCommentNum(self):
        return self.topCommentNum


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        
        self.driver.get("http://www.theguardian.com")
        containers = None
        articles = []

        try:

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-item__comment-count")))
            containers = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fc-item__container")))

        except TimeoutException:
            print "WARNING: TimeoutException containers"
            return
        except NoSuchElementException:
            print "WARNING: No NoSuchElementException containers"
            return

        for index, container in enumerate(containers):

            comment = None
            article = None
            title = None
            href = None
            textTitle = None

            try:
                article = container.find_element_by_css_selector(".fc-item__link")
                title = container.find_element_by_css_selector(".u-faux-block-link__cta")
            except NoSuchElementException:
                print "WARNING: NoSuchElementException article"

##.fc-item__link
##.u-faux-block-link__cta

            try:
                comment = container.find_element_by_css_selector('.js-item__comment-count')
            except NoSuchElementException:
                print "WARNING: NoSuchElementException comment"

            href = article.get_attribute("href")
            textTitle = title.text

            ##WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".u-faux-block-link__overlay")))
            if isinstance(href, basestring) == False or isinstance(textTitle,basestring) == False or len(textTitle) < 4 or len(href) < 10 :
                print "CONTINUE INDEX {}".format(index)
                continue


            commentNumber = 0

            try:
                commentNumber = int(comment.text)
            except ValueError:
                ##print textTitle
                ##print href
                ##print "ValueError Exception comment Number NOT WORKING"
                continue

            if commentNumber > 100:
                art = Article(href, textTitle, commentNumber)
                ##print art.title
                ##print art.url
                ##print art.numComments
                ##print "#####################################################"
                articles.append(art)
        
        print "Total articles: {}".format(len(articles))
        for x in articles:
    ##        print "################################"
    ##        print x.title
    ##        print x.numComments
    ##        print x.url
            topCommentDict = guardian_comment.findTopCommentAndTopNumber(self, x.url)
            x.setTopComment(topCommentDict['topComment'])
            x.setTopCommentNum(topCommentDict['topCommentNumber'])
  ##          print "################################"


        for x in articles:
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print x.title
            print x.numComments
            print x.url
            print x.topComment
            print x.topCommentNum
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

            ##print "TITLE: {} COMMENT_NUMBER: {} LINK: {}".format(textTitle, commentNumber, href)
            ##print "TITLE: {} COMMENT_NUMBER: {} LINK: {}".format(textTitle, commentNumber, href)
            



##23

##container = response.selector.css('.fc-item__container').extract()

##publication: done
##age: depend on the position of the post/the time of the commment
##link: done
##title: done
##number of comments: done
##comment: visit the page
##topComment: visit the page
##type(low priority): depend on the link classification (regular expression)


# for index, container in enumerate(containers):
#     link = container.css('.u-faux-block-link__overlay::attr(href)').extract()[0]
#     print link
#     title = container.css('.u-faux-block-link__overlay::text').extract()[0]
#     print title
#     args = (index, ''.join(container.css('.js-item__comment-count::text').extract()).strip())
#     print 'Article %d : CommentNumber: %s' % args        


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()