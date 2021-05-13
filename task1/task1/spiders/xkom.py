import scrapy
from ..items import Task1Item


class XKomSpider(scrapy.Spider):
    name = 'xkom'
    start_urls = [
        'https://www.x-kom.pl/'
    ]

    def parse(self, response, **kwargs):
        categories = response.css('li.sc-13hctwf-3 a[role="menuitem"]::attr(href)').extract()

        for category in categories:
            yield response.follow(category, callback=self.parse_categories)

    def parse_categories(self, response):
        subcategories = response.css('li.sc-16n31g-4.fcMCVZ ul.sc-16n31g-2.foNRTB li a::attr(href)').extract()

        for subcategory in subcategories:
            yield response.follow(subcategory, callback=self.parse_subcategories)

    def parse_subcategories(self, response):

        items = Task1Item()

        all_products_on_page = response.css('div#listing-container div.sc-1yu46qn-6.kUnYNG.sc-2ride2-0.eYsBmG')

        for product in all_products_on_page:
            product_name = product.css('div.gmIvDY h3::attr(title)').extract()[0]
            price = product.css('div.fpNTm span.hNZEsQ::text').extract()[0]

            items['product_name'] = product_name
            items['price'] = price

            yield items
