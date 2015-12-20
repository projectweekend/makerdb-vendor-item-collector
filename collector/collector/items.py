import scrapy


class CollectorItem(scrapy.Item):

    item_name = scrapy.Field()
    item_url = scrapy.Field()
    item_image_url = scrapy.Field()
    vendor_site = scrapy.Field()
    vendor_name = scrapy.Field()
    vendor_item_id = scrapy.Field()
