import scrapy
from scrapy.http import Request


class RimSpider(scrapy.Spider):
    name = "rim"
    start_urls = ["https://rim.org.ru"]

    def parse_category(self, response):
        products = response.css('div.product-thumb')
        for product in products:
            name = product.css('.product-thumb .caption > a::text').get()
            category = product.css('.nav > li ul li a::text').get()
            price = product.css('.product-thumb .price::text').get()
            link = response.urljoin(product.css('.product-thumb .caption > a::attr(href)').get())
            if price is None:
                price = 'no value'

            yield {
                'name': name,
                'category': category,
                'price': price,
                'link': link
            }

        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)

    def closed(self, reason):
        self.logger.info('Spider closed: %s', reason)