from lxml import html
from requests import get
from pprint import pprint
from pymongo import MongoClient


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36'}
news_list = []

mail_news_link = 'https://news.mail.ru'

mail_response = get(mail_news_link, headers = header)

if mail_response.ok:

    mail_root = html.fromstring(mail_response.text)
    mail_news = mail_root.xpath("//div[contains(@class,'daynews__item')] | //div[contains(@class,'newsitem')]")

    for news in mail_news:
        mail_news_info = {}

        name = news.xpath(".//span[contains(@class,'title')]//text()")
        link_part = news.xpath(".//a[contains(@class,'topnews')]/@href | .//a[contains(@class,'newsite')]/@href")

        if len(link_part) >= 1:

            link = f'{mail_news_link}{link_part[0]}'

            date_mail_response = get(link, headers=header)

            if date_mail_response.ok:

                date_mail_root = html.fromstring(date_mail_response.text)
                date_list = date_mail_root.xpath("//span[@datetime]/@datetime")
                date = date_list[0]

            mail_news_info["source"] = "news.mail.ru"
            mail_news_info["news_name"] = name
            mail_news_info["news_link"] = link
            mail_news_info["news_date"] = date

            news_list.append(mail_news_info)


lenta_news_link = 'https://lenta.ru'

lenta_response = get(lenta_news_link, headers = header)

if lenta_response.ok:

    lenta_root = html.fromstring(lenta_response.text)
    lenta_news = lenta_root.xpath("//div[contains( @class, 'item')]")

    for news in lenta_news:
        lenta_news_info = {}

        link_part = news.xpath(".//a[contains(@href,'/news/')]/@href")

        if len(link_part) >= 1:

            link = f'{lenta_news_link}{link_part[0]}'
            lenta_news_response = get(link, headers=header)

            if lenta_news_response.ok:

                lenta_news_root = html.fromstring(lenta_news_response.text)
                name = lenta_news_root.xpath("//h1[@class='b-topic__title']/text()")
                date = lenta_news_root.xpath("//div[contains( @class, 'b-topic__header')]//time/@datetime")

                lenta_news_info["source"] = "lenta.ru"
                lenta_news_info["news_name"] = name
                lenta_news_info["news_link"] = link
                lenta_news_info["news_date"] = date

                news_list.append(lenta_news_info)

            else:
                continue


yandex_news_link = 'https://yandex.ru/news'

yandex_response = get(yandex_news_link, headers=header)

if yandex_response.ok:

    yandex_root = html.fromstring(yandex_response.text)
    yandex_news = yandex_root.xpath("//a[contains (@href, '/news/story')]/@href")

    for news in yandex_news:
        yandex_news_info = {}

        link = f'{yandex_news_link}{news}'
        yandex_news_response = get(link, headers=header)

        if yandex_news_response.ok:
            yandex_news_root = html.fromstring(yandex_news_response.text)
            name = yandex_news_root.xpath("//span[@class='story__head-wrap']/text()")
            source_agency = yandex_news_root.xpath("//a[contains (@class, 'agency-name')]/text()")

            yandex_news_info["source"] = f"yandex.news / {source_agency}"
            yandex_news_info["news_name"] = name
            yandex_news_info["news_link"] = link

            news_list.append(yandex_news_info)

client = MongoClient('localhost', 27017)
db = client['news']

db.news.insert_many(news_list)
