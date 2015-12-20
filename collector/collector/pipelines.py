import json
import os
from urlparse import urljoin, urlparse
import psycopg2
from scrapy.exceptions import DropItem


DATABASE_URL = os.getenv('MAKERBD_DATABASE_URL')
assert DATABASE_URL
SQL_VENDOR_ITEM_INSERT = 'sp_app_vendor_item_insert'
SQL_VENDOR_ITEM_UPDATE = 'sp_app_vendor_item_update'


def database_connection():
    parsed = urlparse(DATABASE_URL)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    database = parsed.path.strip('/')

    connection = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    connection.set_session(autocommit=True)

    return connection


def item_to_json(item):
    return json.dumps({
        'name': item['item_name'],
        'url': item['item_url'],
        'image_url': item['item_image_url'],
        'vendor_id': item['vendor_item_id'],
        'vendor_name': item['vendor_name'],
        'vendor_site': item['vendor_site']
    })


class ItemPipeline(object):

    def process_item(self, item, spider):
        if not item['vendor_name']:
            raise DropItem('Missing vendor_name')
        if not item['vendor_item_id']:
            raise DropItem('Missing vendor_item_id')
        if not item['vendor_site']:
            raise DropItem('Missing vendor_site')
        if not item['item_name']:
            raise DropItem('Missing item_name')
        if not item['item_url']:
            raise DropItem('Missing item_url')
        if not item['item_image_url']:
            raise DropItem('Missing item_image_url')
        else:
            parsed = urlparse(item['item_image_url'])
            if not parsed.netloc:
                item['item_image_url'] = urljoin(item['vendor_site'], item['item_image_url'])
        return item


class DatabasePipeline(object):

    db = database_connection()

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        item_json = item_to_json(item=item)
        try:
            cursor.callproc(SQL_VENDOR_ITEM_INSERT, [item_json, ])
        except psycopg2.IntegrityError:
            # cursor.callproc(SQL_VENDOR_ITEM_UPDATE, [item_json, ])
            raise DropItem('Duplicate item')
        finally:
            cursor.close()
