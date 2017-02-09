import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy.spiders import Spider

class MySpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wikipedia.org']

    cuisineFile = open('../urlFileRefine.txt','r')
    #start_urls = [line.strip('\n') for line in cuisineFile]

    start_urls = ['https://en.wikipedia.org/wiki/List_of_African_dishes']

    @staticmethod
    def enumerateDishes(selections):
        print 'Enumerate'
        for i, item in enumerate(allSelections):
            isValid = True      #todo: not brackets, not number etc
            if isValid:
                yield {
                        'cuisine': cuisine,
                        'foodItem': item
                    }

    def parse(self, response):
        cuisine = (str(response.url).split('/')[-1])
        #getAllmatchingLi = '//h2[span[contains(., "dishes") or contains(., "dessert") or contains(., "sweet")]]/following-sibling::*[1]//li/b//a[1]/text()'
        #todo: use functions instead. duh
        getAllmatchingLi = '//*[self::h1 or self::h2 or self::h3][span[contains(., "dishes") or contains(., "snacks") or contains(., "dessert") or contains(., "sweet") or contains(., "pasta")]]/following-sibling::*[1]//li//a[1]/text()'
        allSelections = response.xpath(getAllmatchingLi).extract()
        print 'Selection1:' + str(allSelections)
        for i, item in enumerate(allSelections):
            isValid = True      #todo: not brackets, not number etc
            if isValid:
                yield {
                        'cuisine': cuisine,
                        'foodItem': item
                    }

        getAllmatchingLi = '//table[contains(@class, "wikitable sortable")]/tbody//tr//td[1]/a[1]/text()'
        allSelections = response.xpath(getAllmatchingLi).extract()
        print 'Selection2:' + str(allSelections)
        for i, item in enumerate(allSelections):
            isValid = True      #todo: not brackets, not number etc
            if isValid:
                yield {
                        'cuisine': cuisine,
                        'foodItem': item
                    }
