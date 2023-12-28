import scrapy
from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # Parse each quote div 
        for quote in response.css('div.quote'):
            item = QuoteItem()

            item['author'] = quote.css('small.author::text').get()
            item['text'] = quote.css('span.text::text').re(r'“(.+)”')[0]
            item['tags'] = quote.css('div.tags a.tag::text').getall()

            yield item

        # Find the "Next ->" button and follow the link
        for a in response.css('ul.pager a'):
            yield response.follow(a, callback=self.parse)