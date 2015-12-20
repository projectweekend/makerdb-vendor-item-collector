import scrapy
from collector.items import CollectorItem


class AdafruitSpider(scrapy.Spider):

    name = 'adafruit'
    allowed_domains = ['adafruit.com']
    start_urls = [
        'https://www.adafruit.com/category/8',
        'https://www.adafruit.com/category/17',
        'https://www.adafruit.com/category/33',
        'https://www.adafruit.com/category/35',
        'https://www.adafruit.com/category/37',
        'https://www.adafruit.com/category/40',
        'https://www.adafruit.com/category/44',
        'https://www.adafruit.com/category/50',
        'https://www.adafruit.com/category/54',
        'https://www.adafruit.com/category/63',
        'https://www.adafruit.com/category/65',
        'https://www.adafruit.com/category/75',
        'https://www.adafruit.com/category/82',
        'https://www.adafruit.com/category/105',
        'https://www.adafruit.com/category/112',
        'https://www.adafruit.com/category/117',
        'https://www.adafruit.com/category/128',
        'https://www.adafruit.com/category/168',
        'https://www.adafruit.com/category/196',
        'https://www.adafruit.com/category/203',
        'https://www.adafruit.com/category/227',
        'https://www.adafruit.com/category/234',
        'https://www.adafruit.com/category/290',
        'https://www.adafruit.com/category/307',
        'https://www.adafruit.com/category/342'
    ]
    xpath_for = {
        'product_url': '//div[@class="row product-listing"]//h1/a/@href',
        'product_info': '//div[@class="row product-info"]',
        'name': '//div[@id="prod-right-side"]/h1/text()',
        'img_src': '//div[@id="prod-primary-img-container"]//img/@src',
        'product_id': '//div[@class="product_id"]/text()'
    }

    def parse(self, response):
        for item in response.selector.xpath(self.xpath_for['product_url']):
            url = response.urljoin(item.extract())
            yield scrapy.Request(url=url, callback=self.parse_product_info)

    def parse_product_info(self, response):
        try:
            info = response.selector.xpath(self.xpath_for['product_info'])[0]
        except IndexError:
            print('No product info for: {0}'.format(response.url))
        else:
            item_name = info.xpath(self.xpath_for['name']).extract_first().strip()
            item_url = response.url
            item_image_url = info.xpath(self.xpath_for['img_src']).extract_first().strip()
            vendor_site = 'https://www.adafruit.com'
            vendor_name = 'Adafruit'
            vendor_item_id = info.xpath(self.xpath_for['product_id']).extract_first()
            try:
                vendor_item_id = vendor_item_id.split(':')[1].strip()
            except IndexError:
                vendor_item_id = ''

            yield CollectorItem(
                item_name=item_name,
                item_url=item_url,
                item_image_url=item_image_url,
                vendor_site=vendor_site,
                vendor_name=vendor_name,
                vendor_item_id=vendor_item_id)
