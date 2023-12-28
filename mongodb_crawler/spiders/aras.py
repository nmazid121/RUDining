import scrapy
from ..items import FoodItem

class ArasSpider(scrapy.Spider):
    name = "aras"
    allowed_domains = ["arashotchicken.com"]
    start_urls = ["https://arashotchicken.com"]

    def parse(self, response):
    # Parsing the divs for food items! : ) # andre and noob
        for food in response.css('li.eJXTXb') :
            item = FoodItem()

            item['foodName'] = food.css('h4.uKXCDd::text').get()

            yield item