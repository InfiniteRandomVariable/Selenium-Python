from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import re
import time
import common_classes
from threading import Thread


##REQUIRE
##obtain timestamp or anything else about this page before calling this method because it will switch to iframe.

def findTopCommentAndTopNumber(browser, article, COMMENT_NUM_CRITERIA,VOTEUP_CRITERIA ):
    resultDict = {}
    WORD_LIMITS = 150
    print "inside disqus"
    ##browser.switch_to.frame("dsq-2")
    try:
        frame = WebDriverWait(browser, 130).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"iframe#dsq-2")))
        browser.switch_to.frame(frame)
    except Exception:
        print "#################### EXCEPTION fail to switch iframe"
        return resultDict
    comNum = 0
    ##.comment-count
    try:      
        elm = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment-count")))
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
        browser.switch_to.default_content();
        return resultDict

    ##//a[@href='#disqus_thread']
    ##.dropdown-toggle
    ##try
    ##//a[@data-sort='popular']

    try:
        ##xpath
        ##//a[@data-nav="conversation"]
        ##".dropdown-toggle"
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-nav='conversation'][@data-toggle='dropdown']"))).click()
        
    except Exception:
        browser.switch_to.default_content();
        print "############# EXCEPTION //a[@data-nav='conversation']"
        return resultDict



    try:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-sort='popular']"))).click()
    except Exception as e:
        print "################### EXCEPTION a[@data-sort='popular']"
        browser.switch_to.default_content();
        return resultDict

    ##a data-role="username"
    print "TIME SLEEP"
    time.sleep(3)
    ##.updatable.count
    topCommentNumber = 0
    try:
        elm = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".updatable.count")))
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
        browser.switch_to.default_content();
        return resultDict



    


    ##.post-message


    """BROWSER UI: LOAD COMMENTS"""
   


    """Old page links should be gone"""


    topComment = ''


    try:
        topComment = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".post-message>p"))).text.strip()[0:WORD_LIMITS]
        if len(topComment) > (WORD_LIMITS -1):
            topComment = "%s..." % topComment
#        for elm in elms[:]:
 #           topComment = topComment + ' ' + elm.text

    except Exception as e:
        print "NoSuchElementException /TimeoutException .content__dateline>time"
        browser.switch_to.default_content();
        return resultDict


    topComment = re.sub(r'\\', "",topComment.strip())

    if len (topComment) < 10:
        print "top comment"
        browser.switch_to.default_content();
        return resultDict

    ##itemprop="datePublished"
    ##.content__dateline>time                

    print "DONE Top Comment: %s TopCommentNumber: %s commentNum: %s" % (topComment, topCommentNumber, comNum)
    article.topComment = topComment
    article.topCommentNum = topCommentNumber
    article.numComments = comNum

    browser.switch_to.default_content()


    resultDict = {'topComment':topComment, 'topCommentNumber':topCommentNumber,'numComments': comNum}
    return resultDict
