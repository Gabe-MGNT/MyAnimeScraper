# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import pickle
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.request import fingerprint

class AnimeScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AnimeScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

import logging
from scrapy.item import Item
logger = logging.getLogger(__name__)
from scrapy.http import Request

class DuplicatesMiddleware:

    def __init__(self):
        self.cache_file = "visited_links"
        self.visited_links = set()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        try:
            with open("{}.pkl".format(self.cache_file), "rb") as file:
                self.visited_links = pickle.load(file)
                print("Loaded {} visited links".format(len(self.visited_links)))
        except FileNotFoundError:
            self.visited_links = set()

    def spider_closed(self, spider):
        spider.logger.info("Storing all visited links")
        print(self.visited_links)
        try:
            with open("{}.pkl".format(self.cache_file), 'wb') as f:
                pickle.dump(self.visited_links, f)
        except Exception as e:
            raise(e)
        
        spider.logger.info("All links have been put in file")
        spider.logger.info("Spider closed: %s" % spider.name)

    

    
    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            if isinstance(i, Request):

                if i.url in self.visited_links:
                    spider.logger.info("\nIgnoring already visited: %s\n" % i.url)
                    continue



            elif isinstance(i, Item):
                self.visited_links.add(response.request.url)

 
            yield i

    


        