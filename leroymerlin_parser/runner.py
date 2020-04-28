from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin_parser import settings
from leroymerlin_parser.spiders.leroymerlin import LeroyMerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    object_to_search = input("Введите название категории для сбора данных: ")

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyMerlinSpider, object_to_search=object_to_search)

    process.start()