from selenium import webdriver
from scrapy.spider import BaseSpider 


class ProductSpider(BaseSpider):
    name = "product_spider"
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_odkw=books&_osacat=0&_trksid=p2045573.m570.l1313.TR0.TRC0.Xpython&_nkw=python&_sacat=0&_from=R40']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
##	print "about to start waiting"
##	self.driver.implicitly_wait(600)
##	print "finish waiting"
	counter = 0
        while True:
            next = self.driver.find_element_by_xpath('//td[@class="pagn-next"]/a')

            try:
                if counter < 4: 
			next.click()
			counter += 1
			print counter
		else:
			print "over five"
			break

                # get the data and write it to scrapy items
            except:
                break

        self.driver.close()
