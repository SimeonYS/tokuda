import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import TokudaItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class TokudaSpider(scrapy.Spider):
	name = 'tokuda'
	start_urls = ['https://www.tokudabank.bg/bg/za-bankata/novini/?page=1']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="h5 g-color-black g-font-weight-600 mb-3"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="text-center"]/a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//time//text()').get().strip()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="g-mb-30"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=TokudaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
