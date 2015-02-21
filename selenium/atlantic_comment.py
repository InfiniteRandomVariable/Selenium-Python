import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import atlantic_time
import re
import time, articleUtil
from threading import Thread

# find this image http://www.theatlantic.com/features/archive/2015/02/consent-isnt-enough-in-fifty-shades-of-grey/385267/ 

def findTopCommentAndTopNumber(self, url,isFirstPage ,WAIT_SECONDS):

    print "pre 1"
    self.driver.get(url)
    if isFirstPage == False:
        time.sleep(WAIT_SECONDS)   

    print "pre 2"
    resultDict = {}
    ##CHANGE
    ##VOTEUP_CRITERIA = 8
    #DIVIDER = 3
    VOTEUP_CRITERIA = 2
    ##CHANGE
    ##COMMENT_NUM_CRITERIA = 65
    COMMENT_NUM_CRITERIA = 10
    WORDS_LIMIT = 140

    try:
        ##.welcome-lightbox-continue
        elm = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".welcome-lightbox-continue")))
        elm.click()
    except Exception:
        print "Exception fail to click .welcome-lightbox-continue"

    title = ''
    template = ''
    HEADLINE = ".headline"
    HED = ".hed"
    print("pre 3")
    for cssPath in [HEADLINE,HED]:
        try:
            ##headline
            elm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,cssPath)))
            if elm:
                template = cssPath
                title = elm.text.strip()
                break

        except Exception as e:
            print "#################### Exception problem Title2: {}".format(e)


    if len(title) < 3:
        return resultDict

    timeStamp = None


    ## interesting XPATH matching technique
    ##_time = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//time[@itemprop='datePublished']")))
    print("pre 4")
    for time_css_selector in ["time"]:
        try:
            _time = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"time")))
            timeStamp = atlantic_time.timeToTimeStamp(_time.get_attribute("datetime"))

            print("TimeStamp: {}".format(timeStamp))

            if timeStamp and timeStamp > 1000:
                break
        except Exception as e:
            print "timeError can't find the element %s " % e

    if timeStamp is None or timeStamp < 1000:
        print "*****************ERROR Timestamp Error"
        return resultDict

##.jump-to-comments>a
    print("pre 5")
    try:
        elm = None

        if template == HEADLINE:
            elm = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".jump-to-comments>a")))
        elif template == HED:
            elm = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".social-icon.comments")))

        elm.click()
    except Exception as e:
        self.driver.switch_to.default_content();
        print "####################### EXCEPTION just to comment"
        return

    print("pre 6")
    ##self.driver.switch_to.frame("dsq-2")
    time.sleep(WAIT_SECONDS)
    try:
        frame = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"iframe#dsq-2")))
        self.driver.switch_to.frame(frame)
    except Exception:
        print "#################### EXCEPTION fail to switch iframe"
        return resultDict
    comNum = 0
    ##.comment-count

    print("pre 7")

    try:      
        elm = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment-count")))
        text = elm.text
        print "Time Text %s" % text
        numText = re.search( r'\d+[^\S]', text)
        print "numText: %s" % numText.group()
        try:
            comNum = int(numText.group().strip())
        except Exception:
            print "**************EXCEPTION comment Number"
    except Exception as e:
        print "############################# EXCEPTION problem comment count %s" % e

    if comNum < COMMENT_NUM_CRITERIA:
        self.driver.switch_to.default_content();
        return resultDict

    print("pre 8")
    ##//a[@href='#disqus_thread']
    ##.dropdown-toggle
    ##try
    ##//a[@data-sort='popular']

    try:
        ##xpath
        ##//a[@data-nav="conversation"]
        ##".dropdown-toggle"
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-nav='conversation'][@data-toggle='dropdown']"))).click()
        
    except Exception:
        self.driver.switch_to.default_content();
        print "############# EXCEPTION //a[@data-nav='conversation']"
        return resultDict


    print("pre 9")

    try:
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-sort='popular']"))).click()
    except Exception as e:
        print "################### EXCEPTION a[@data-sort='popular']"
        self.driver.switch_to.default_content();
        return resultDict

    ##a data-role="username"
    print("pre 10")
    time.sleep(5)
    ##.updatable.count
    topCommentNumber = 0
    try:
        elm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".updatable.count")))
        text = elm.text
        if isinstance(text, basestring) and len(text) > 0:
            try:
                topCommentNumber = int(text)
            except Exception as e:
                print "############# EXCEPTION fail to convert ot number"

    except Exception as e:
        print "#######################EXCEPTION Comment Number"

    if topCommentNumber < VOTEUP_CRITERIA:
        print "RETURNING Small Number"
        self.driver.switch_to.default_content();
        return resultDict



    


    ##.post-message


    """BROWSER UI: LOAD COMMENTS"""
   


    """Old page links should be gone"""


    topComment = ''

    print("pre 10")

    try:
        firstComment = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".post-message")))
        
        elms = firstComment.find_elements_by_css_selector('p')[0:2]
        for elm in elms[:]:
            if not elm.text:
                try:
                    _elm = elm.find_element_by_css_selector('i')
                except Exception as ee:
                    print("Exception: {0}".format(ee))
                if _elm.text:
                    topComment = topComment + ' ' + _elm.text
            else:
                topComment = topComment + ' ' + elm.text
            #print("topComment1: {0}".format(topComment))

    except Exception as e:
        print("Except: fail to find this element {0}".format(e))
        self.driver.switch_to.default_content();
        return resultDict

    #print("topComment2: {0}".format(topComment))
    topComment = re.sub(r'\\', "",topComment.strip())
    #print("topComment3: {0}".format(topComment))

    if len (topComment) < 10:
        print "top comment"
        self.driver.switch_to.default_content();
        return resultDict

    topComment = articleUtil.truncatedStringForRow(topComment);
    
    self.driver.switch_to.default_content();

    ##.photo>img
    ##<img height="458" width="570" itemprop="image" style="width: 100% !important;height:auto !important" src="//cdn.theatlantic.com/static/newsroom/img/mt/2015/02/HillaryBaby/lead.jpg?njdcj8"/>

    # if len(topComment) > WORDS_LIMIT:
    #     _topC = topComment[0:WORDS_LIMIT]
    #     tpC = re.sub(r'\.*$',"",_topC)
    #     topComment = "%s..." % tpC

    ##itemprop="datePublished"
    ##.content__dateline>time                

    #print "DONE Top Comment: %s TopCommentNumber: %s Timestamp: %s CommentNum: %s Title: %s" % (topComment, topCommentNumber, timeStamp, comNum, title)
    resultDict = {'topComment':topComment, 'topCommentNumber':topCommentNumber,'timeStamp': timeStamp, 'numComments': comNum, 'title': title}
    return resultDict
