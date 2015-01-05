import scrapy

class Audiobookbay(scrapy.Spider):
				name = 'Audiobookbat'

				def __init__(self, category=None, *args, **kwargs):
								super(Audiobookbay, self).__init__(*args, **kwargs)
								self.start_urls = ['http://audiobookbay.to/audio-books/type/%s/' % category]


