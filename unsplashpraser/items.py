# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
import re

def process_name(value: str):
    value = value[0].strip()
    return value

def process_photo(value: str):
    pattern = r'src="([^"]+)"'
    match = re.search(pattern, value)
    if match:
        image_url = match.group(1)
        return image_url
    else:
        return None

def process_categor(value: str):
    return value

class UnsplashpraserItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo))
    categoria = scrapy.Field(input_processor=Compose(process_categor), output_processor=TakeFirst())
    _id = scrapy.Field()
