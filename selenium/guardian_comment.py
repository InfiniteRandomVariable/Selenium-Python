import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import guardian_time,time,re


#TOP_COMMENT_NUM_XPATH = '//div[contains(concat(' ',normalize-space(@class),' '), "d-comment__inner d-comment__inner--top-level")]/div[2]/div[@data-recommend-count]/span[1]/span[1]'
TOP_COMMENT_NUM_XPATH = '//div[contains(concat(' ',normalize-space(@class),' '), "d-comment__inner d-comment__inner--top-level")]/div[2]/div[1]/span[1]/span[1]'
#TOP_COMMENT_NUM_XPATH = '//div[contains(concat(' ',normalize-space(@class),' '), "d-comment__inner d-comment__inner--top-level")]/div/div[@data-recommend-count]/span/span[contains(concat(' ',normalize-space(@class),' '), "d-comment__recommend-count--old")]'
TOP_COMMENT_CONTAINER_CSS = '.d-comment__inner.d-comment__inner--top-level .d-comment__content'
TOP_COMMENT_CSS = '.d-comment__main .d-comment__body>p'
TOP_COMMENT_NUM_CSS = '.d-comment__recommend-count--old'
#TOP_COMMENT_XPATH = '//div[contains(concat(' ',normalize-space(@class),' '), "d-comment__inner d-comment__inner--top-level")]/div/div[@data-recommend-count]/span/span'
def findComment(self, currentTopCommentNum):
    #XPATH //div/@data-recommend-count
    # //div[@data-recommend-count]
    #/div[@data-recommend-count]
    #.d-comment__inner.d-comment__inner--top-level .d-comment__content .d-comment__main .d-comment__body>p

    #select one class by XPATH        
    #//div[contains(concat(" ", normalize-space(@class), " "), " d-comment__main ")]
    #CSS_PATH for selecting top level comments .d-comment__inner.d-comment__inner--top-level .d-comment__content
    #//div[contains(concat(' ',normalize-space(@class),' '), "ok yes")]
    #//div[contains(concat(' ',normalize-space(@class),' '), "d-comment__inner d-comment__inner--top-level")]/
    oldNum = currentTopCommentNum
    print "find Comment 0: currentTopCommentNum: %s" % currentTopCommentNum
    currentIndex = 0
    print "find Comment 1"
    topCommentContainers = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,TOP_COMMENT_CONTAINER_CSS)))
    
    #topCommentNumElms = self.driver.find_elements_by_xpath(TOP_COMMENT_NUM_XPATH)
    print "find Comment 2"
    #topCommentNumElms = element.find_elements_by_xpath(TOP_COMMENT_NUM_XPATH)
    _commentText = ""
    for index, container in enumerate(topCommentContainers[:]):
        print "find Comment 3"
        try:

            if not container: continue

            elm = container.find_element_by_css_selector(TOP_COMMENT_NUM_CSS)
            if not elm: continue
            _text = elm.text
            if not _text or len(_text) == 0: continue

            num = int(_text.strip())
            print "find Comment 4 index"
            if num > currentTopCommentNum:

                print "find Comment 5: new %s old %s oldIndex: %s newIndex:%s" % (num, currentTopCommentNum, currentIndex, index)
                currentTopCommentNum = num
                currentIndex = index
                textElm = container.find_element_by_css_selector(TOP_COMMENT_CSS)
                if not textElm: continue
                _commentText = textElm.text.strip()


        except Exception as e:
            print "Error in converting currentTopCommentNum %s" % e

    if _commentText and len(_commentText) > 1 and currentTopCommentNum > oldNum:
        return [_commentText, currentTopCommentNum]
    else:
        return




    # print "find Comment 6 finalIndex: %s oldNum %s newNum %s " % (currentIndex, oldNum, currentTopCommentNum)

    # if oldNum == currentTopCommentNum: return

    # print "find Comment 6.1 finalIndex: %s oldNum %s newNum %s " % (currentIndex, oldNum, currentTopCommentNum)

    ##Todo: use XPATH to reduce to one seek only and obtain the number of the row from the css index above
    # comElm = self.driver.find_elements_by_css_selector(TOP_COMMENT_CSS)[currentIndex]
    # if not comElm: return

    # textElm = comElm.find_element_by_xpath('p')
    # if not textElm: return

    # commentText = textElm.text.strip()
    # print "find Comment 7"
    # if commentText and len(commentText)> 1:
    #     print "find Comment 8"
    #     print "CommentText: %s CommentNum: %s" % (commentText, currentTopCommentNum)
    #     return [commentText, currentTopCommentNum]

    # print "find Comment 9"




def findTopCommentAndTopNumber(self, page, isFirstPage,WAIT_SECONDS):

    print "pre 1"
    URL = "%s#comments" % page.url
    self.driver.get(URL)

    if isFirstPage == False:
        time.sleep(WAIT_SECONDS)   

    counter = 0
    comm = None

    try:
        print "pre 2"
        timeElm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//time")))
        print "pre 2.1"
        if not timeElm:
            print "pre 2.2"
            return page


        timeText = timeElm.get_attribute("datetime")
        print "pre 3"
        page.age = guardian_time.guardianTimeToTimeStamp(timeText)

        # numComments = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.commentcount2__value'))).text.strip()
        # numStr = re.sub(r'\D',"",numComments)
        # print "numComment %s" % numStr

        # page.numComments = int(numStr)

    except Exception as e:
        print "findTopCommentAndTopNumber: %s" % e
        return page

    """BROWSER UI: LOAD COMMENTS"""

    if isFirstPage:
        try:
            print "pre 4"
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-controls='comments-order-popup']"))).click()
            print "pre 5"
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-link-name='comments-oldest']"))).click()
            print "AFTER CLICK OLDEST"
        except Exception as e:
            print "Unexpected viewMore %s" % e
            
        time.sleep(WAIT_SECONDS+5)

    # try:
    #     WebDriverWait(self.driver, 5).until(EC.staleness_of(comm))
    #     print "d-comment__body 2"
    # except TimeoutException:
    #     print "TimeoutException .d-comment__body";

    """Old page links should be gone"""
    pageLinks = None
    commentAndCommentNum = ["", 10]

    def findCommentProcedure(_self,_currentTopCommentNum, _currentTopComment, _commentAndCommentNum):
        originalCommentAndNum = _commentAndCommentNum[:]
        newCommentAndCommentNum = findComment(_self, originalCommentAndNum[1])
        if newCommentAndCommentNum and isinstance(newCommentAndCommentNum, list) and len (newCommentAndCommentNum) == 2:
            num = newCommentAndCommentNum[1]
            if num > originalCommentAndNum[1]:
                print "num: %s" % num
                return newCommentAndCommentNum
            else:
                return originalCommentAndNum
        else:
            return originalCommentAndNum

    try:
        print "currentTopComment 0"
        pageLinks = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.pagination__list>a')))[0:2]
        print "currentTopComment 1"
        currentTopComment = ""
        currentTopCommentNum = 10
        for index, link in enumerate(pageLinks[:]):
            print "currentTopComment 2"
            
            if not link: continue

            pageLinkURL = link.get_attribute('href')
            if 'new' in pageLinkURL:
                print "ERROR URL: shouldn't contain new %s" % pageLinkURL
                continue
    
            if index > 0:
                link.click()
                time.sleep(WAIT_SECONDS)
            print "currentTopComment 3"
            commentAndCommentNum = findCommentProcedure(self, currentTopCommentNum, currentTopComment, commentAndCommentNum)[:]
            # commentAndCommentNum = findComment(self, currentTopCommentNum)
            # if commentAndCommentNum and isinstance(commentAndCommentNum, list) and len (commentAndCommentNum) == 2:
            #     num = commentAndCommentNum[1]
            #     if num > currentTopCommentNum:
            #         print "num: %s" % num
            #         currentTopCommentNum = commentAndCommentNum[1]
            #         currentTopComment = commentAndCommentNum[0]
                

        if not pageLinks or len(pageLinks) == 0:
            commentAndCommentNum = findCommentProcedure(self, currentTopCommentNum, currentTopComment, commentAndCommentNum)[:]

        
        page.topComment = commentAndCommentNum[0]
        page.topCommentNum = commentAndCommentNum[1]

        print "currentTopCommentText %s" % page.topComment
        print "currentTopCommentNum %s" % page.topCommentNum
        
    except Exception as e:
        print "Unexpected .button.button--small.button--tertiary.pagination__action.js-discussion-change-page %s" % e
    return page




    # seen = set()

    # for index, link in enumerate(pageLinks):

    #     print 'BEFORE COMMENT PAGE: {}'.format(index)
        
    #     sublink = None
    #     try:
    #         sublink = self.driver.find_elements_by_css_selector('.button.button--small.button--tertiary.pagination__action.js-discussion-change-page')[index] 
    #     except Exception as e:
    #         print "Unexpected exceptions {}".format(e)
    #         continue


    #     """Capture the first comment here"""     
    #     href = sublink.get_attribute('href')
    #     oldComments = None

    #     if href not in seen:
    #         try:
    #             oldComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
    #         except Exception as e:
    #             print "Unexpected exceptions {}".format(e)
    #             continue

    #         seen.add(href)
    #         sublink.click()
    #         print "HREF: {}".format(href)
        
    #         isOldCommentGone = False
    #         for cnt, oldComment in enumerate(oldComments):
    #             if isOldCommentGone:
    #                 break
    #             try:
    #                 WebDriverWait(self.driver, 3).until(EC.staleness_of(oldComment))
    #                 isOldCommentGone = True
    #                 print 'PAGE {} OLD COMMENTS {}'.format(index, cnt)
    #             except TimeoutException:
    #                 print "TimeoutException Old Comments"
    #             except Exception as e:
    #                 print "Unexpected d-comment__inner.d-comment__inner--top-level: {}".format(e)

    #         try:
    #             num = 0
    #             newComments = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".d-comment__inner.d-comment__inner--top-level")))
    #             for idx, newComment in enumerate(newComments):
    #                 print 'BEFORE PAGE: {} COMMENT: {}'.format(index, idx)
    #                 try:
    #                     numText = newComment.find_element_by_css_selector('.d-comment__recommend-count--old')
    #                     num = int(numText.text)
    #                 except Exception as e:
    #                     print "Unexpected d-comment__recommend-count--old: {}".format(e)
                        
    #                 if isinstance( num, int ) and num > topCommentNumber:
    #                     topCommentNumber = num
    #                     _topComment = newComment.find_element_by_css_selector('.d-comment__body')
    #                     topComment = _topComment.text
    #                     print 'AFTER PAGE: {}'.format(index)
    #                     print 'TOP Number: {} COMMENT: {}'.format(topCommentNumber, topComment.encode('utf-8'))
    #         except TimeoutException:
    #             print "TimeoutException New Comments"
    #         except Exception as e:
    #             print "Unexpected New Comments"
                               

    # print "DONE Top Comment: {} TopCommentNumber: {} Timestamp: {}".format(topComment.encode('utf-8'), topCommentNumber, timeStamp)
    # seen.clear()
    # resultDict = {'topComment':topComment, 'topCommentNumber':topCommentNumber,'timeStamp': timeStamp}
    # return resultDict

