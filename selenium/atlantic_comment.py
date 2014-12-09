import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import atlantic_time
import re
import time
from threading import Thread


def findTopCommentAndTopNumber(self, url):

    print "pre 1"
    self.driver.get(url)
    print "pre 2"
    resultDict = {}
    ##CHANGE
    ##VOTEUP_CRITERIA = 8
    VOTEUP_CRITERIA = 2
    ##CHANGE
    ##COMMENT_NUM_CRITERIA = 65
    COMMENT_NUM_CRITERIA = 10

    try:
        ##.welcome-lightbox-continue
        elm = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".welcome-lightbox-continue")))
        elm.click()
    except Exception:
        print "Exception fail to click .welcome-lightbox-continue"

    title = ''
    try:
        ##headline
        elm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".headline")))
        titleText = elm.text
        if isinstance(titleText, basestring):
            title = titleText.strip()
   
    except (NoSuchElementException, TimeoutException) as e:
        print "#################### Exception Title1: {}".format(e)
    except Exception as e:
        print "#################### Exception Title2: {}".format(e)

    if len(title) < 3:
        return resultDict

    timeStamp = None

    try:
        _time = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//time[@itemprop='datePublished']")))
        timeStamp = atlantic_time.timeToTimeStamp(_time.get_attribute("datetime"))
        print "timeStamp: %s" % timeStamp
    except Exception as e:
        print "NoSuchElementException /TimeoutException //time[@itemprop='datePublished'] %s " % e
        self.driver.switch_to.default_content();
        return resultDict

    if timeStamp is None or timeStamp < 1000:
        print "*****************ERROR Timestamp Error"
        self.driver.switch_to.default_content();
        return resultDict

##.jump-to-comments>a

    try:
        elm = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".jump-to-comments>a")))
        elm.click()
    except Exception as e:
        self.driver.switch_to.default_content();
        print "####################### EXCEPTION just to comment"
        return

    
    ##self.driver.switch_to.frame("dsq-2")
    try:
        frame = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"iframe#dsq-2")))
        self.driver.switch_to.frame(frame)
    except Exception:
        print "#################### EXCEPTION fail to switch iframe"
        return resultDict
    comNum = 0
    ##.comment-count
    try:      
        elm = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment-count")))
        text = elm.text
        print "Time Text %s" % text
        if isinstance(text, basestring) and len(text) > 0:
            numText = re.search( r'^\d+\S', text)
            print "numText: %s" % numText.group()
            try:
                comNum = int(numText.group())
            except Exception:
                print "**************EXCEPTION comment Number"
    except Exception as e:
        print "############################# EXCEPTION comment count %s" % e

    if comNum < COMMENT_NUM_CRITERIA:
        self.driver.switch_to.default_content();
        return resultDict

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



    try:
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-sort='popular']"))).click()
    except Exception as e:
        print "################### EXCEPTION a[@data-sort='popular']"
        self.driver.switch_to.default_content();
        return resultDict

    ##a data-role="username"
    print "TIME SLEEP"
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


    try:
        firstComment = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".post-message")))
        
        elms = firstComment.find_elements_by_css_selector('p')
        for elm in elms[:]:
            topComment = topComment + ' ' + elm.text

    except Exception as e:
        print "NoSuchElementException /TimeoutException .content__dateline>time"
        self.driver.switch_to.default_content();
        return resultDict


    topComment = topComment.strip()

    if len (topComment) < 10:
        print "top comment"
        self.driver.switch_to.default_content();
        return resultDict

    ##itemprop="datePublished"
    ##.content__dateline>time                

    print "DONE Top Comment: %s TopCommentNumber: %s Timestamp: %s CommentNum: %s Title: %s" % (topComment, topCommentNumber, timeStamp, comNum, title)
    resultDict = {'topComment':topComment, 'topCommentNumber':topCommentNumber,'timeStamp': timeStamp, 'numComments': comNum, 'title': title}
    return resultDict