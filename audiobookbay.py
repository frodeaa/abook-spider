# -*- coding: utf-8 -*-

import scrapy

class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()

class Audiobookbay(scrapy.Spider):
    name = 'Audiobookbat'

    def __init__(self, category=None, *args, **kwargs):
        super(Audiobookbay, self).__init__(*args, **kwargs)
        self.start_urls = ['http://audiobookbay.to/audio-books/type/%s/' % category]

    def parse(self, resp):
        # fetch book details (if any)
        for name in resp.xpath('//div[@class="postTitle"]/h1/text()').extract():
            item = BookItem()
            item['id'] = resp.url
            item['name'] = name
            yield item

        # fetch url to book details page
        for url in resp.xpath('//span[@class="postLink"]/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

        # fetch url to next page
        #for url in resp.xpath('//div[@class="wp-pagenavi"]/a[not(@title)]/@href').extract():
        #    yield scrapy.Request(url, callback=self.parse)

