import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import guardian_time,time




def findTopCommentAndTopNumber(self, url, isFirstPage,WAIT_SECONDS):

    print "pre 1"
    self.driver.get(url)
    if isFirstPage == False:
        time.sleep(WAIT_SECONDS)   

    print "pre 2"
    resultDict = {}
##  print "about to start waiting"
##  print "finish waiting"

    counter = 0
    comm = None
    try:
        comm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".d-comment__body")))
    except (NoSuchElementException, TimeoutException) as e:
        print "NoSuchElementException TimeoutException .d-comment__body"
        return resultDict

    timeStamp = None
    try:
        time = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".content__dateline>time")))
        timeStamp = guardian_time.guardianTimeToTimeStamp(time.get_attribute("datetime"))
    except (NoSuchElementException, TimeoutException) as e:
        print "NoSuchElementException /TimeoutException .content__dateline>time"
        return resultDict

    if timeStamp is None or timeStamp < 1000::
        print "*****************ERROR Timestamp Error"
        return resultDict

    """BROWSER UI: LOAD COMMENTS"""

    try:

        print "pre 3"
        viewMore1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-controls='comments-order-popup']")))
        print "pre 4"
        viewMore1.click()
        print "FirstClick"

        viewMore = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-link-name='comments-oldest']")))

        viewMore.click()
        print "AFTER CLICK OLDEST"
    except TimeoutException:
        print "First click TimeoutException viewMore"
        return resultDict
    except ElementNotVisibleException:
        print "ElementNotVisibleException viewMore"
        return resultDict
    except Exception as e:
        print "Unexpected viewMore"
        return resultDict

    try:
        WebDriverWait(self.driver, 5).until(EC.staleness_of(comm))
        print "d-comment__body 2"
    except TimeoutException:
        print "TimeoutException .d-comment__body";

    comm = 0; 


    """Old page links should be gone"""
    try:
        print "CONFIRM BUTTON GONE"
        pageLinks = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')
        
        for index, link in enumerate(pageLinks):
            print 'BEFORE COMMENT PAGE: {}'.format(index)
            if index > 0:
                WebDriverWait(self.driver, 5).until(EC.staleness_of(link))
            print 'AFTER COMMENT PAGE: {}'.format(index)
    except (TimeoutException, NoSuchElementException) as e:
        print "TimeoutException PAGENATION"
    except Exception as e:
        print "Unexpected .button.button--small.button--tertiary.pagination__action.js-discussion-change-page"
        


    topComment = ''
    topCommentNumber = 5

    pageLinks = None 
    try:
        pageLinks = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')
    except Exception as e:
        print "Unexpected exceptions {}".format(e)
        return resultDict


    seen = set()

    for index, link in enumerate(pageLinks):

        print 'BEFORE COMMENT PAGE: {}'.format(index)
        
        sublink = None
        try:
            sublink = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')[index] 
        except Exception as e:
            print "Unexpected exceptions {}".format(e)
            continue


        """Capture the first comment here"""     
        href = sublink.get_attribute('href')
        oldComments = None

        if href not in seen:
            try:
                oldComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
            except Exception as e:
                print "Unexpected exceptions {}".format(e)
                continue

            seen.add(href)
            sublink.click()
            print "HREF: {}".format(href)
        
            isOldCommentGone = False
            for cnt, oldComment in enumerate(oldComments):
                if isOldCommentGone:
                    break
                try:
                    WebDriverWait(self.driver, 3).until(EC.staleness_of(oldComment))
                    isOldCommentGone = True
                    print 'PAGE {} OLD COMMENTS {}'.format(index, cnt)
                except TimeoutException:
                    print "TimeoutException Old Comments"
                except Exception as e:
                    print "Unexpected d-comment__inner.d-comment__inner--top-level: {}".format(e)

            try:
                num = 0
                newComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
                for idx, newComment in enumerate(newComments):
                    print 'BEFORE PAGE: {} COMMENT: {}'.format(index, idx)
                    try:
                        numText = newComment.find_element_by_css_selector('.d-comment__recommend-count--old')
                        num = int(numText.text)
                    except Exception as e:
                        print "Unexpected d-comment__recommend-count--old: {}".format(e)
                        
                    if isinstance( num, int ) and num > topCommentNumber:
                        topCommentNumber = num
                        _topComment = newComment.find_element_by_css_selector('.d-comment__body')
                        topComment = _topComment.text
                        print 'AFTER PAGE: {}'.format(index)
                        print 'TOP Number: {} COMMENT: {}'.format(topCommentNumber, topComment.encode('utf-8'))
            except TimeoutException:
                print "TimeoutException New Comments"
            except Exception as e:
                print "Unexpected New Comments"
                               

    print "DONE Top Comment: {} TopCommentNumber: {} Timestamp: {}".format(topComment.encode('utf-8'), topCommentNumber, timeStamp)
    seen.clear()
    resultDict = {'topComment':topComment, 'topCommentNumber':topCommentNumber,'timeStamp': timeStamp}
    return resultDict

