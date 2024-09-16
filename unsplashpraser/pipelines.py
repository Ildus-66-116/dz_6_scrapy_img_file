# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import csv
from scrapy.pipelines.images import ImagesPipeline

def write_to_csv(file_path, data):
    """Запись в csv"""
    fieldnames = set()
    for d in data:
        fieldnames.update(d.keys())
    fieldnames = sorted(fieldnames)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


class UnsplashpraserPipeline:

    def __init__(self):
        self.unsplash = []

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.unsplash.append(item_dict)
        return item

    def close_spider(self, spider):
        write_to_csv(f'{spider.name}.csv', self.unsplash)


class UnspPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
