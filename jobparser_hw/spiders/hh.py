# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser_hw.items import JobparserItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response:HtmlResponse):
        # next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href")
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in vacansy_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.css('div.vacancy-title h1::text').extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        link = response.url
        # print(name,salary)
        yield JobparserItem(name=name, salary=salary, link=link)

