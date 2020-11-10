# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import LeroyMerlinParserItem
from scrapy.loader import ItemLoader

class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, object_to_search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={object_to_search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        object_links = response.xpath("//a[contains (@class, 'product-name-inner')]/@href").extract()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in object_links:
            yield response.follow(link, callback=self.object_parse)

    def object_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinParserItem(), response=response)
        loader.add_xpath("name", "//h1[@class='header-2']/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//picture[@slot='pictures']//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_value("link", response.url)
        loader.add_xpath("characteristics_term", "//dt[@class='def-list__term']/text()")
        loader.add_xpath("characteristics_def", "//dd[@class='def-list__definition']/text()")

        # name = response.xpath("//h1[@class='header-2']/text()").extract_first()
        # price = response.xpath("//span[@slot='price']/text()").extract_first()
        # characteristics = response.xpath("//dl[@class='def-list']").extract()
        # photos = response.xpath("//picture[@slot='pictures']//source[@media=' only screen and (min-width: 1024px)']/@srcset").extract()
        # link = response.url
        yield loader.load_item()
