import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy.spiders import Spider
from wiki.items import WikiItem

import re
import string

class MySpider(scrapy.Spider):
    name = 'wikiSpider'
    allowed_domains = ['wikipedia.org']
    #start_urls = ['https://en.wikipedia.org/wiki/List_of_cuisines',
    #                'https://en.wikipedia.org/wiki/List_of_African_dishes',
    #                'https://en.wikipedia.org/wiki/List_of_Argentine_dishes']

    cuisineFile = open('../wikiCuisineLinkExtractor/urlFileRefine.txt','r')
    start_urls = [line.strip('\n') for line in cuisineFile]

    def parse(self, response):

        #to debug values on first run
        for item in self.parseSecPages(response):
            yield item

        cuisineDiv = "//div[contains(@class, 'div-col columns column-width')]//li/a/@href"
        cuisineList = response.xpath(cuisineDiv).extract()

        for i, cuisine in enumerate(cuisineList):
            self.log('Cuisines ' + str(i) + ': ' + str(cuisine))
            yield scrapy.Request(
                response.urljoin(str(cuisine)),
                callback=self.parseSecPages
            )

    def parseSecPages(self, response):
        cuisineUrl = str(response.url).split('/')[-1]
        cuisine = self.getCuisine(cuisineUrl)

        getAllmatchingLi = ['//*[self::h1 or self::h2 or self::h3][span[contains(., "dishes") or contains(., "snacks") or contains(., "dessert") or contains(., "sweet") or contains(., "pasta")]]/following-sibling::*[1]//li//a[1]/text()'
                            ,"//table[contains(@class,'wikitable sortable')]//tr/td[1]//text()"
                            ,"//div[@id='mw-content-text']//ul//li/b//text()"
                            #,"//div[@id='mw-content-text']/div[@class='div-col columns column-width']//ul/li/a/text()"
                            ]

        for matcher in getAllmatchingLi:
            allSelections = response.xpath(matcher).extract()
            for i, item in enumerate(allSelections):
                self.log('Item ' + str(i) + "::" + cuisine +' : ' + str(item.encode('utf-8')))

                regMatch = re.match('[A-Za-z0-9 ]+',item)
                if(self.is_ascii(item) and regMatch and item.strip):
                    yield WikiItem (cuisine = cuisine, foodItem = item)
                else:
                    self.log('Not a valid item : ' + item)

    def getCuisine(self, url):
        regMatch = re.match('List_of_(\w+)_dishes', url)
        regMatch2 = re.match('(_?\w+_?)_cuisines', url)
        if regMatch:
            return regMatch.group(1)
        elif regMatch2 :
            return regMatch2.group(1)
        else:
            return url

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)
