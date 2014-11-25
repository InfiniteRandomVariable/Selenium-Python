import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import guardian_comment, timeHelper



class Article:
   
    def __init__(self, url, title, numComments):
        self.url = url
        self.title = title
        self.numComments = numComments
        self.topComment = ''
        self.age = 0
        self.topCommentNum = 0


    @property   
    def url(self):
        return self.url
    @property    
    def title(self):
        return self.title
    @property    
    def numComments(self):
        return self.numComments
    @property            
    def topComment(self):
        return self.topComment
    @property    
    def topCommentNum(self):
        return self.topCommentNum
    @property
    def age(self):
        return self.age

    @topComment.setter    
    def topComment(self, value):
        self.topComment = value
    @topCommentNum.setter
    def topCommentNum(self, value):
        self.topCommentNum = value
    @age.setter        
    def age(self, value):
        self.age = value




class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        
        self.driver.get("http://www.theguardian.com")
        containers = None
        articles = []
        COMMENT_NUM_CRITERIA = 300

        try:

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-item__comment-count")))
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

            ##WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".u-faux-block-link__overlay")))
            if isinstance(href, basestring) == False or isinstance(textTitle,basestring) == False or len(textTitle) < 4 or len(href) < 10 :
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
                art = Article(href, textTitle, commentNumber)
                ##print art.title
                ##print art.url
                ##print art.numComments
                ##print "#####################################################"
                articles.append(art)

        articleLen = len(articles)
        for x in articles:

            topCommentDict = guardian_comment.findTopCommentAndTopNumber(self, x.url).copy()

            if isinstance (topCommentDict,dict) == False or isinstance (topCommentDict,dict) and len(topCommentDict) == 0:
                print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
                articles.remove(x)
                print ""
                continue

            for key, value in topCommentDict.iteritems():
                print "Key NOV25 {} Value{}".format(key, value)
            
                if 'topComment' == key and isinstance(value, basestring):
                    x.topComment = value
                elif 'topCommentNumber' == key and isinstance(value, int):
                    x.topCommentNum = value
                elif 'timeStamp' == key and isinstance(value, int):
                    x.age = value
                else:
                    print "REMOVED TITLE {}".format(x.title.encode('utf-8'))
                    articles.remove(x)
                    print ""
                    continue


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
        for x in articles:
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print x.title
            print x.numComments
            print x.url
            print x.topComment
            print x.topCommentNum
            print x.age
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




