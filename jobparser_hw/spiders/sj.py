# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser_hw.items import JobparserItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains (@class, 'f-test-button-dalshe')]/@href")
        yield response.follow(next_page, callback=self.parse)

        vacansy_links = response.xpath("//a[contains (@class, '_1UJAN')]/@href").extract()

        for link in vacansy_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[contains (@class, '_3mfro')]").extract_first()
        salary = response.xpath("//span[contains (@class, 'ZON4b')]/text()").extract()
        link = response.url
        yield JobparserItem(name=name, salary=salary, link=link)


