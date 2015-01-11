# -*- coding: utf-8 -*-

import scrapy
from urlparse import urljoin
import summary_tool

class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    format = scrapy.Field()
    bitrate = scrapy.Field()
    is_abridged = scrapy.Field()
    peers = scrapy.Field()
    seeds = scrapy.Field()
    total_size = scrapy.Field()
    count_downloads = scrapy.Field()
    torrent_url = scrapy.Field()
    cover_url = scrapy.Field()
    long_text = scrapy.Field()
    summary = scrapy.Field();


class Audiobookbay(scrapy.Spider):
    name = 'Audiobookbay'

    def __init__(self, category=None, limit=1, *args, **kwargs):
        super(Audiobookbay, self).__init__(*args, **kwargs)
        self.limit = limit
        self.category = category
        if limit and int(limit) > 1:
            self.start_urls = ['http://audiobookbay.to/audio-books/type/%s/page/%s' %
                     (category, page) for page in range(1, int(limit) + 1)]
        else:
            self.start_urls = ['http://audiobookbay.to/audio-books/type/%s/' % category]

    def parse(self, resp):
        # fetch book details (if any)
        for name in resp.xpath('//div[@class="postTitle"]/h1/text()').extract():
            item = BookItem()
            item['id'] = resp.url
            item['name'] = name
            item['category'] = self.category
            for key in ['author', 'format', 'bitrate', 'is_abridged']:
                query = '//p[@style="left;"]/span[@class="%s"]/text()' % key
                for v in resp.xpath(query).extract():
                    item[key] = v

            kv = {"peers": "Peers:", "seeds": "Seeds:",
                    "total_size": "Combined File Size:",
                    "count_downloads": "Completed Downloads:" }
            for k in kv:
                query = "//tr[td[text()='%s']]/td/text()" % kv[k]
                for v in resp.xpath(query).extract():
                    item[k] = v

            for v in resp.xpath("//a[starts-with(@href, '/download.php?f')]/@href").extract():
                item['torrent_url'] = urljoin(resp.url, v)

            for img in resp.xpath("//div[@class='postContent']/div/p/a/img/@src").extract():
                item['cover_url'] = img

            for text in resp.xpath("//div[@class='postContent']/p[@style='left;']/text()").extract():
                text = text.rstrip("\r\n").lstrip("\r\n")
                item['long_text'] = text
                item['summary'] = text
                if len(text) > 100:
                    st = summary_tool.SummaryTool()
                    sentences_dic = st.get_senteces_ranks(text)
                    item['summary'] = st.get_summary("", text, sentences_dic).lstrip("\r\n")

            yield item

        # fetch url to book details page
        for url in resp.xpath('//span[@class="postLink"]/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

        # fetch url to next category page, traverse all pages
        if self.limit == '0':
            for url in resp.xpath('//div[@class="wp-pagenavi"]/a[not(@title)]/@href').extract():
                yield scrapy.Request(url, callback=self.parse)

