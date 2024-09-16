import scrapy
from scrapy.http import HtmlResponse
from sbor_and_razmetka_data.dz.dz_6_scrapy_img_file.unsplashpraser.items import UnsplashpraserItem
from scrapy.loader import ItemLoader


class UnsplashcomSpider(scrapy.Spider):
    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@itemprop="contentUrl"]')
        for link in links:
            print()
            yield response.follow(link, callback=self.parse_img)

    def parse_img(self, responce: HtmlResponse):
        loader = ItemLoader(item=UnsplashpraserItem(), response=responce)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', responce.url)
        loader.add_xpath('photos', "//img[contains(@src, 'images')]")
        loader.add_xpath('categoria', '//div[@class="RAoiG uoMSP fSX9S Dh164"]/a/text()')
        yield loader.load_item()
