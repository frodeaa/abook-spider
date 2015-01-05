# -*- coding: utf-8 -*-

import scrapy

class Audiobookbay(scrapy.Spider):
    name = 'Audiobookbat'

    def __init__(self, category=None, *args, **kwargs):
        super(Audiobookbay, self).__init__(*args, **kwargs)
        self.start_urls = ['http://audiobookbay.to/audio-books/type/%s/' % category]

    def parse(self, resp):
        for url in resp.xpath('//div[@class="wp-pagenavi"]/a[not(@title)]/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

