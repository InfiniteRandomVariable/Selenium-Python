 #Using Scrapy with Selenium to scape a rendered page [Updated]
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
     
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
     
##from selenium import selenium
from selenium import webdriver
     
    ##from linkedpy.items import LinkedPyItem
     
class LinkedPySpider(InitSpider):
    name = 'guardian'
    allowed_domains = ['www.theguardian.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ["http://www.linkedin.com/csearch/results?type=companies&keywords=&pplSearchOrigin=GLHD&pageKey=member-home&search=Search#facets=pplSearchOrigin%3DFCTD%26keywords%3D%26search%3DSubmit%26facet_CS%3DC%26facet_I%3D80%26openFacets%3DJO%252CN%252CCS%252CNFR%252CF%252CCCR%252CI"]
 
    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        print "####################init"
        ##self.selenium = selenium("localhost", 4444, "*firefox", "http://www.linkedin.com")
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.theguardian.com")
        print "111111111111111init"
        self.log("nnn Starting the Selenium Server! nnn")
        ##self.selenium.start()
        print "2222222222222222init"

        self.log("nnn Successfully, Started the Selenium Server! nnn")
 
    def __del__(self):
        self.driver.close()
        print self.verificationErrors
        CrawlSpider.__del__(self)
 
    def init_request(self):
        #"""This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)
 
    def login(self, response):
        #"""Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'session_key': 'email@address.com', 'session_password': 'password'},
                    callback=self.check_login_response)
 
    def check_login_response(self, response):
        #"""Check the response returned by a login request to see if we aresuccessfully logged in."""
        if "Sign Out" in response.body:
            self.log("nnnSuccessfully logged in. Let's start crawling!nnn")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log("nnnFailed, Bad times :(nnn")
            """below for testing only"""	
            return self.initialized()
            # Something went wrong, we couldn't log in, so nothing happens.
 
    def parse(self, response):
        hxs = HtmlXPathSelector(response)        
        sel = self.selenium
        ##sel.open(response.url)
        ##time.sleep(2.5)
        print 'PARSEING DONE'
       ## sites = sel.select('//ol[@id='result-set']/li')
        items = []
        # for site in sites:
        #     item = LinkedPyItem()
        #     item['title'] = site.select('h2/a/text()').extract()
        #     item['link'] = site.select('h2/a/@href').extract()
        #     items.append(item)
        return items


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

