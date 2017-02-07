import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy.spiders import Spider
#from wiki import WikicuItem

class MySpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_cuisines']

    #itemsDiscovered = 0

    def parse(self, response):
        cuisineDiv = "//div[contains(@class, 'div-col columns column-width')]//li/a/@href"
        cuisineList = response.xpath(cuisineDiv).extract()

#        yield scrapy.Request(
#            response.urljoin('Malaysian_Indian_cuisine'),
#            callback=self.parseSecPages
#        )

        for i, cuisine in enumerate(cuisineList):
            self.log('Cuisines ' + str(i) + ': ' + str(cuisine))
            yield scrapy.Request(
                response.urljoin(str(cuisine)),
                callback=self.parseSecPages
            )
        self.log('============ Final count' + str(itemsDiscovered))

    def parseSecPages(self, response):
        self.log("sec parsing at " + str(response))
        cuisine = str(response).split('/')[-1]
        getAllmatchingLi = '//h2[span[contains(., "dishes") or contains(., "dessert") or contains(., "sweet")]]/following-sibling::*[1]//li/b//a[1]/text()'
        getAllmatchingLi = '//*[self::h1 or self::h2 or self::h3][span[contains(., "dishes") or contains(., "snacks") or contains(., "dessert") or contains(., "sweet") or contains(., "pasta")]]/following-sibling::*[1]//li//a[1]/text()'

        allSelections = response.xpath(getAllmatchingLi).extract()
        #self.log('============' + str(allSelections))

        for i, item in enumerate(allSelections):
            self.log('Item ' + str(i) + "::" + cuisine +' : ' + str(item.encode('utf-8')))
            #itemsDiscovered += 1

            if True:
                yield {
                        'cuisine': cuisine,
                        'foodItem': item
                    }


    def parse_cuisine_page(self, response):
        self.logger.info('**********Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item

    def parse_sec_pages(self, response):
        self.logger.info('**********Hi, this is sec page parser! %s', response.url)
        return
