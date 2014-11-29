import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import guardian_comment, timeHelper, common_classes
from urlparse import urlparse




class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        ##self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)


    def classifyTag(tag):
        if tag =='commentisfree':
            return 'opinion'
        else:
            return tag


    def test_search_in_python_org(self):
        
        
        DOMAIN_URL = "http://www.theguardian.com"
        containers = None
        articles = []
        MAX_NUM_ARTICLES = 10
        COMMENT_NUM_CRITERIA = 200
        TOP_COMMENT_STRING_LEN = 20
        TOP_COMMENT_NUM = 10
        DEFAULT_TIME = 1416691395

        self.driver.get(DOMAIN_URL)

        try:

            WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-item__comment-count")))
            containers = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fc-item__container")))

        except TimeoutException:
            print "WARNING: TimeoutException containers"
            return
        except NoSuchElementException:
            print "WARNING: No NoSuchElementException containers"
            return
        except Exception as e:
            print "WARNING: Expected containers: {}".format(e)
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
            except Exception as e:
                print "WARNING: NoSuchElementException article"
                continue

##.fc-item__link
##.u-faux-block-link__cta

            try:
                comment = container.find_element_by_css_selector('.js-item__comment-count')
            except:
                print "WARNING: NoSuchElementException comment"
                continue

            href = article.get_attribute("href")
            textTitle = title.text

            tag = urlparse(href).path.split('/')[1]


            if isinstance(tag, basestring) == False or len(tag) < 2 or tag =='football'or tag == 'sport':
                continue
            ##WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".u-faux-block-link__overlay")))
            if isinstance(textTitle,basestring) == False or len(textTitle) < 4:
                print "CONTINUE INDEX {}".format(index)
                continue

            commentNumber = 0
            try:
                commentNumber = int(comment.text)
            except ValueError:
                continue
            except Exception as e:
                continue

            

            if commentNumber > COMMENT_NUM_CRITERIA:
                art = common_classes.Article(href, textTitle, commentNumber)
                _tag = classifyTag(tag)
                art.tag = _tag
                ##print art.title
                ##print art.url
                ##print art.numComments
                ##print "#####################################################"
                articles.append(art)

            if len (articles) > MAX_NUM_ARTICLES:
                break

        articleLen = len(articles)

        for x in articles[:]:

            topCommentDict = guardian_comment.findTopCommentAndTopNumber(self, x.url).copy()

            if isinstance (topCommentDict,dict) == False or isinstance (topCommentDict,dict) and len(topCommentDict) == 0:
                print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
                articles.remove(x)
                print ""
                continue

            for key, value in topCommentDict.iteritems():
                print "Key NOV25 %s Value %s" % (key, value)
            
                if 'topComment' == key and isinstance(value, basestring) and len(value) > TOP_COMMENT_STRING_LEN:
                    x.topComment = value
                elif 'topCommentNumber' == key and isinstance(value, int) and value > TOP_COMMENT_NUM:
                    x.topCommentNum = value
                elif 'timeStamp' == key and isinstance(value, int) and value > DEFAULT_TIME:
                    x.age = value
                else:
                    print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
                    articles.remove(x)
                    print ""
                    break


            # if topCommentDict is None or topCommentDict and len(topCommentDict) != 3:
            #     print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
            #     articles.remove(x)
            #     continue;
            
            ##qualifying the object attributes
            # if isinstance(_comm, str) and len(_comm) > 5 and isinstance(_commNum, int) and _commNum > 1 and isinstance(_age, int) and _age > 1:
            #     print "ADD TITLE: {} AGE: {%f} TOP COM NUMBER: {%f} \n COMMNET {}".format(x.title.encode('utf-8'), _age, _commNum, _comm.encode('utf-8'))
            #     x.setTopComment(_comm)
            #     x.setTopCommentNum(_commNum)
            #     x.setAge(_age)
            # else:
            #     print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
            #     articles.remove(x)
            #     continue

  ##          print "################################"

        timeHelper.sortTimeForGuardian(articles)
        print "BEFORE Total articles: {} AFTER Total articles: {}".format(articleLen, len(articles))
        for x in articles[:]:
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print x.title
            print x.numComments
            print x.url
            print x.topComment
            print x.topCommentNum
            print x.age
            print x.tag
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




