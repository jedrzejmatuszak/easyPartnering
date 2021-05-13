import scrapy
from ..items import Task1Item


class XKomSpider(scrapy.Spider):
    name = 'xkom'
    start_urls = [
        'https://www.x-kom.pl/'
    ]

    def parse(self, response, **kwargs):
        categories = response.css('li.sc-13hctwf-3 a[role="menuitem"]::attr(href)').extract()
        yield {'categories': categories}

        for category in categories:
            yield response.follow(category, callback=self.parse_categories)

    def parse_categories(self, response):
        subcategories = response.css('li.sc-16n31g-4.fcMCVZ ul.sc-16n31g-2.foNRTB li a::attr(href)').extract()
        yield {'subcategories': subcategories}

        for subcategory in subcategories:
            yield response.follow(subcategory, callback=self.parse_subcategories)

    def parse_subcategories(self, response):

        items = Task1Item()

        product_name = response.css('div.sc-1yu46qn-12.gmIvDY a h3::attr(title)').extract()
        price = response.css('div.sc-1yu46qn-16.fpNTm span.hNZEsQ::text').extract()

        items['product_name'] = product_name
        items['price'] = price

        yield items


class Test(scrapy.Spider):
    name = 'Test'
    start_urls = [
        'https://www.x-kom.pl/g-2/c/159-laptopy-notebooki-ultrabooki.html'
    ]

    def parse(self, response, **kwargs):

        items = Task1Item()

        all_products_on_page = response.css('div#listing-container')

        for product in all_products_on_page:
            product_name = product.css('div.kUnYNG div.gmIvDY h3::attr(title)').extract()
            price = product.css('div.fpNTm span.hNZEsQ::text').extract()

            items['product_name'] = product_name
            items['price'] = price

            yield items