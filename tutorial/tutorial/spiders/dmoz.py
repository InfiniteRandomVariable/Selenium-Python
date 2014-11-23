from selenium import selenium
from selenium import webdriver
from scrapy.spider import BaseSpider
from datetime import datetime 
##import os

class ProductSpider(BaseSpider):
    name = "product_spider"
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_odkw=books&_osacat=0&_trksid=p2045573.m570.l1313.TR0.TRC0.Xpython&_nkw=python&_sacat=0&_from=R40']

    def __init__(self):

##	chromedriver = "/usr/local/bin/"
##	os.environ["webdriver.chrome.driver"] = chromedriver
##	driver = webdriver.Chrome(chromedriver)
##	driver.get("http://stackoverflow.com")
##	driver.quit()
##	return

        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
##	print "about to start waiting"
##	print "finish waiting"

	counter = 0
        while True:
            next = self.driver.find_element_by_xpath('//td[@class="pagn-next"]/a')

            try:
                if counter < 5: 
                    next.click()
                    counter += 1
                    now = datetime.utcnow()
                    print 'Counter:{} Time:{}'.format(counter,now)
                    self.driver.implicitly_wait(300)
                    now = datetime.utcnow()
                    print 'Counter:{} Time:{}'.format(counter,now)
                    print '##################################'
                    
                else:
                    print "over five"
                    self.driver.close()
                    break
                # get the data and write it to scrapy items
            except:
                self.driver.close()
                break
        ##self.driver.close()

# ##   from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
# from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# # Create a new instance of the Firefox driver
# driver = webdriver.Firefox()

# # go to the google home page
# driver.get("http://www.google.com")

# # the page is ajaxy so the title is originally this:
# print driver.title

# # find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")

# # type in the search
# inputElement.send_keys("cheese!")

# # submit the form (although google automatically searches now without submitting)
# inputElement.submit()

# try:
#     # we have to wait for the page to refresh, the last thing that seems to be updated is the title
#     WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

#     # You should see "cheese! - Google Search"
#     print driver.title

# finally:
#     driver.quit()




# from selenium.webdriver.common.action_chains import ActionChains
# element = driver.find_element_by_name("source")
# target =  driver.find_element_by_name("target")

# ActionChains(driver).drag_and_drop(element, target).perform()
