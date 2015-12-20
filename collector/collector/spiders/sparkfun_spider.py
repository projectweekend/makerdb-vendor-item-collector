import scrapy
from collector.items import CollectorItem


class SparkfunSpider(scrapy.Spider):

    name = 'sparkfun'
    allowed_domains = ['sparkfun.com']
    start_urls = [
        'https://www.sparkfun.com/categories/103?page=all',
        'https://www.sparkfun.com/categories/273?page=all',
        'https://www.sparkfun.com/categories/176?page=all',
        'https://www.sparkfun.com/categories/20?page=all',
        'https://www.sparkfun.com/categories/70?page=all',
        'https://www.sparkfun.com/categories/51?page=all',
        'https://www.sparkfun.com/categories/2?page=all',
        'https://www.sparkfun.com/categories/4?page=all',
        'https://www.sparkfun.com/categories/272?page=all',
        'https://www.sparkfun.com/categories/276?page=all',
        'https://www.sparkfun.com/categories/157?page=all',
        'https://www.sparkfun.com/categories/76?page=all',
        'https://www.sparkfun.com/categories/53?page=all',
        'https://www.sparkfun.com/categories/233?page=all',
        'https://www.sparkfun.com/categories/31?page=all',
        'https://www.sparkfun.com/categories/23?page=all',
        'https://www.sparkfun.com/categories/46?page=all',
        'https://www.sparkfun.com/categories/204?page=all',
        'https://www.sparkfun.com/categories/97?page=all',
        'https://www.sparkfun.com/categories/16?page=all'
    ]
    xpath_for = {
        'product_url': '//div[contains(@class, "tile product-tile")]/div[@class="actions-wrap"]/a/@href',
        'product_info': '//div[@class="row product"]',
        'name': '//div[@class="hidden-sm hidden-xs"]/div[@class="product-title"]/h1/text()',
        'img_src': '//div[@id="images-carousel-wrap"]//div[@class="item active"]/img/@src',
        'product_id': '//div[@class="hidden-sm hidden-xs"]/div[@class="product-title"]/div[@class="sku"]/text()'
    }

    def parse(self, response):
        pass
        for item in response.selector.xpath(self.xpath_for['product_url']):
            url = response.urljoin(item.extract())
            yield scrapy.Request(url=url, callback=self.parse_product_info)

    def parse_product_info(self, response):
        try:
            info = response.selector.xpath(self.xpath_for['product_info'])[0]
        except IndexError:
            print('No product info for: {0}'.format(response.url))
        else:
            item_name = info.xpath(self.xpath_for['name']).extract_first()
            item_url = response.url
            item_image_url = info.xpath(self.xpath_for['img_src']).extract_first()
            vendor_site = 'https://www.sparkfun.com'
            vendor_name = 'Sparkfun'
            vendor_item_id = info.xpath(self.xpath_for['product_id']).extract_first()
            try:
                vendor_item_id = vendor_item_id.split('-')[1].strip()
            except IndexError:
                vendor_item_id = ''

            yield CollectorItem(
                item_name=item_name,
                item_url=item_url,
                item_image_url=item_image_url,
                vendor_site=vendor_site,
                vendor_name=vendor_name,
                vendor_item_id=vendor_item_id)
