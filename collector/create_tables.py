from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.types import STRING
from boto.exception import JSONResponseError


def main():
    try:
        Table.create(
            'makerdb_vendor_items',
            schema=[
                HashKey('vendor_name', data_type=STRING),
                RangeKey('vendor_item_id', data_type=STRING)
            ],
            throughput={
                'read': 1,
                'write': 1
            }
        )
        print('Table created: makerdb_vendor_items')
    except JSONResponseError as e:
        print(e.message)


if __name__ == '__main__':
    main()
