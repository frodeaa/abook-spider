# -*- coding: utf-8 -*-

import scrapy

class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    format = scrapy.Field()
    bitrate = scrapy.Field()
    is_abridged = scrapy.Field()
    peers = scrapy.Field()
    seeds = scrapy.Field()
    total_size = scrapy.Field()


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
            for key in ['author', 'format', 'bitrate', 'is_abridged']:
                query = '//p[@style="left;"]/span[@class="%s"]/text()' % key
                for v in resp.xpath(query).extract():
                    item[key] = v

            kv = {"peers": "Peers:", "seeds": "Seeds:", "total_size": "Combined File Size:" }
            for k in kv:
                query = "//tr[td[text()='%s']]/td/text()" % kv[k]
                for v in resp.xpath(query).extract():
                    item[k] = v

            scrapy.log.msg(">>CD %s " % resp.xpath("//tr[td[text()='Completed Downloads:']]/td/text()").extract())
            scrapy.log.msg(">>D %s " % resp.xpath("//a[starts-with(@href, '/download.php?f')]/@href").extract())

            yield item

        # fetch url to book details page
        for url in resp.xpath('//span[@class="postLink"]/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

        # fetch url to next page
        #for url in resp.xpath('//div[@class="wp-pagenavi"]/a[not(@title)]/@href').extract():
        #    yield scrapy.Request(url, callback=self.parse)

