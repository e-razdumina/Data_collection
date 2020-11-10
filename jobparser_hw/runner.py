from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser_hw import settings
from jobparser_hw.spiders.hh import HhSpider
from jobparser_hw.spiders.sj import SjSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider)
    process.crawl(SjSpider)

    process.start()