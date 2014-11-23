import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException



def findTopCommentAndTopNumber(self, url):

    print "pre 1"
    self.driver.get(url)
    print "pre 2"
##  print "about to start waiting"
##  print "finish waiting"

    counter = 0
    ##viewMore = self.driver.find_element_by_css_selector('.discussion__show-button.button--show-more.button.button--large.button--primary.js-discussion-show-button')
    ##viewMore = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.discussion__show-button.button--show-more.button.button--large.button--primary.js-discussion-show-button')))
    ##.//*[@id='comments-order-popup']/li[2]/button
    comm = self.driver.find_element_by_css_selector(".d-comment__body")
    print "d-comment__body 1"
    """BROWSER UI: LOAD COMMENTS"""

    try:
    ##aria-controls="comments-order-popup"
    ##viewMore1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,".//div[@id='comments']/div/div/div[2]/div[4]/div[1]/button")))    
        ##viewMore1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-controls='comments-order-popup']")))
        print "pre 3"
        viewMore1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[@aria-controls='comments-order-popup']")))
        print "pre 4"
        viewMore1.click()
        print "FirstClick"
        ##data-link-name="comments-oldest"
        ##driver.findElement(By.xpath("//div[@data-link-name='comments-oldest']"))
        ##driver.findElement(By.xpath("//div[@_celltype='celltype']"))
        viewMore = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-link-name='comments-oldest']")))
        ##viewMore = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//ul[@id='comments-order-popup']/li[2]/button")))
        viewMore.click()
        print "AFTER CLICK OLDEST"
    except TimeoutException:
        print "First click TimeoutException"

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


    topComment = ''
    topCommentNumber = 5

    pageLinks = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')
    seen = set()

    for index, link in enumerate(pageLinks):

        print 'BEFORE COMMENT PAGE: {}'.format(index)
        
        sublink = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')[index] 
        """Capture the first comment here"""     
        href = sublink.get_attribute('href')

        if href not in seen:
            oldComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
            seen.add(href)
            sublink.click()
            print "HREF: {}".format(href)
        
            
            for cnt, oldComment in enumerate(oldComments):
                try:
                    WebDriverWait(self.driver, 6).until(EC.staleness_of(oldComment))
                    print 'PAGE {} OLD COMMENTS {}'.format(index, cnt)
                except TimeoutException:
                    print "TimeoutException Old Comments"

            try:
                num = 0
                newComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
                for idx, newComment in enumerate(newComments):
                    print 'BEFORE PAGE: {} COMMENT: {}'.format(index, idx)
                    try:
                        numText = newComment.find_element_by_css_selector('.d-comment__recommend-count--old')
                        print numText.text
                        num = int(numText.text)
                        ##num = int(numText)
                    except NoSuchElementException:
                        print "NO SuchElementException"
                    # num = 1
                    if isinstance( num, int ) and num > topCommentNumber:
                        topCommentNumber = num
                        _topComment = newComment.find_element_by_css_selector('.d-comment__body')
                        topComment = _topComment.text
                        print 'AFTER PAGE: {}'.format(index)
                        print 'TOP Number: {} COMMENT: {}'.format(topCommentNumber, topComment)
            except TimeoutException:
                print "TimeoutException New Comments"

    print "DONE Top Comment: {} TopCommentNumber: {}".format(topComment, topCommentNumber)
    seen.clear()
    return {'topComment':topComment, 'topCommentNumber':topCommentNumber}

