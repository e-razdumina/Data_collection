from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd


def vacancies_pars():
    vacancy_name = input("Введите название профессии для поиска вакансий: ")
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36'}
    vacancies_final_list = []

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    vacancies_final_list = []

    hh_main_link = 'https://hh.ru/search/vacancy'
    hh_page_count = 0

    hh_html = requests.get(
        f'{hh_main_link}?L_save_area=true&clusters=true&enable_snippets=true&text={vacancy_name}&showClusters=true',
        headers=header).text
    hh_soup = bs(hh_html, 'html.parser')

    hh_total_vacancies = hh_soup.find('h1', {'class': 'bloko-header-1'}).getText()
    hh_total_vacancies = int(re.sub('\D', '', hh_total_vacancies))
    hh_pages_max = int(hh_soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})[-1].getText())

    print(
        f'На портале hh.ru было найдено {hh_total_vacancies} вакансий {vacancy_name}. К обработке доступно {hh_pages_max} страниц')
    hh_pages_to_process = int(input('Введите число страниц на обработку: '))

    while hh_pages_to_process < 0 or hh_pages_to_process > hh_pages_max:
        hh_pages_to_process = int(input('Вы ввели неверно число. Повторите ввод: '))

    for i in range(hh_pages_to_process):
        hh_html = requests.get(
            f'{hh_main_link}?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&text={vacancy_name}&page={i}',
            headers=header).text
        hh_soup = bs(hh_html, 'html.parser')

        hh_vacancies_block = hh_soup.find_all('div', {'class': 'vacancy-serp'})[0]
        hh_vacancies_list = hh_vacancies_block.find_all('div', {'class': 'vacancy-serp-item'})

        for vacancy in hh_vacancies_list:
            hh_vacancy_data = {}

            hh_vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
            hh_vacancy_company = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'}).getText()
            hh_vacancy_company = re.sub("\W", " ", hh_vacancy_company)
            hh_vacancy_city = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()
            hh_vacancy_link = vacancy.find('a')['href']
            hh_vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()

            if len(hh_vacancy_salary) > 1:
                hh_vacancy_salary_status = hh_vacancy_salary.split(' ')

                if hh_vacancy_salary_status[0] == 'от':
                    hh_vacancy_salary_max = None
                    hh_vacancy_salary_min = hh_vacancy_salary_status[1]
                    hh_vacancy_salary_min = int(re.sub("\D", "", hh_vacancy_salary_min))
                    hh_vacancy_salary_currency = hh_vacancy_salary_status[2]

                elif hh_vacancy_salary_status[0] == 'до':
                    hh_vacancy_salary_max = hh_vacancy_salary_status[1]
                    hh_vacancy_salary_max = int(re.sub("\D", "", hh_vacancy_salary_max))
                    hh_vacancy_salary_min = None
                    hh_vacancy_salary_currency = hh_vacancy_salary_status[2]

                else:
                    hh_vacancy_salary_currency = hh_vacancy_salary_status[1]
                    hh_vacancy_salary = hh_vacancy_salary_status[0].split('-')
                    hh_vacancy_salary_min = hh_vacancy_salary[0]
                    hh_vacancy_salary_min = int(re.sub("\D", "", hh_vacancy_salary_min))
                    hh_vacancy_salary_max = hh_vacancy_salary[1]
                    hh_vacancy_salary_max = int(re.sub("\D", "", hh_vacancy_salary_max))
            else:
                hh_vacancy_salary_currency = None
                hh_vacancy_salary_min = None
                hh_vacancy_salary_max = None

            hh_vacancy_data['name'] = hh_vacancy_name
            hh_vacancy_data['company'] = hh_vacancy_company
            hh_vacancy_data['city'] = hh_vacancy_city
            hh_vacancy_data['salary_min'] = hh_vacancy_salary_min
            hh_vacancy_data['salary_max'] = hh_vacancy_salary_max
            hh_vacancy_data['currency'] = hh_vacancy_salary_currency
            hh_vacancy_data['link'] = hh_vacancy_link
            hh_vacancy_data['site'] = 'hh.ru'

            vacancies_final_list.append(hh_vacancy_data)

        hh_page_count += 1

    hh_vacancies_count = len(vacancies_final_list)
    print(
        f'Было обработано {hh_page_count} страниц выдачи hh.ru. Была собрана информация о {hh_vacancies_count} вакансиях')

    sj_main_link = 'https://russia.superjob.ru'
    sj_page_count = 0

    sj_html = requests.get(f'{sj_main_link}/vacancy/search/?keywords={vacancy_name}', headers=header).text
    sj_soup = bs(sj_html, 'html.parser')

    sj_total_vacancies = sj_soup.find('span', {'class': '_3mfro _1ZlLP _2JVkc _2VHxz'}).getText()
    sj_total_vacancies = int(re.sub('\D', '', sj_total_vacancies))
    sj_pages_max = int(sj_soup.find_all('span', {'class': '_3IDf-'})[-3].getText())

    print(
        f'На портале sj.ru было найдено {sj_total_vacancies} вакансий {vacancy_name}. К обработке доступно {sj_pages_max} страниц')
    sj_pages_to_process = int(input('Введите число страниц на обработку: '))

    while sj_pages_to_process < 0 or sj_pages_to_process > sj_pages_max:
        sj_pages_to_process = int(input('Вы ввели неверно число. Повторите ввод: '))

    for i in range(sj_pages_to_process):
        sj_html = requests.get(
            f'{sj_main_link}/vacancy/search/?keywords={vacancy_name}&page={i}',
            headers=header).text
        sj_soup = bs(sj_html, 'html.parser')

        sj_vacancies_list = sj_soup.find_all('div', {'class': 'f-test-vacancy-item'})

        for vacancy in sj_vacancies_list:
            sj_vacancy_data = {}

            sj_vacancy_name = vacancy.find('div', {'class': 'CuJz5'}).getText()
            sj_vacancy_company = vacancy.find('span', {'class': 'f-test-text-vacancy-item-company-name'}).getText()
            sj_vacancy_city = vacancy.find('span', {'class': 'f-test-text-company-item-location'}).getText()
            sj_vacancy_city = sj_vacancy_city.split(' ')[2]
            sj_vacancy_city = re.sub("\W", "", sj_vacancy_city)
            sj_vacancy_link = sj_main_link + vacancy.find('a')['href']
            sj_vacancy_salary = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).getText()

            if len(sj_vacancy_salary) > 1:
                sj_vacancy_salary_status = sj_vacancy_salary.split(' ')

                if sj_vacancy_salary_status[0] == 'от':
                    sj_vacancy_salary_max = None
                    sj_vacancy_salary_min = int(re.sub("\D", "", sj_vacancy_salary))
                    sj_vacancy_salary_currency = sj_vacancy_salary_status[-1]

                elif sj_vacancy_salary_status[0] == 'до':
                    sj_vacancy_salary_max = int(re.sub("\D", "", sj_vacancy_salary))
                    sj_vacancy_salary_min = None
                    sj_vacancy_salary_currency = sj_vacancy_salary_status[-1]

                elif sj_vacancy_salary_status[0] == 'По':
                    sj_vacancy_salary_min = None
                    sj_vacancy_salary_max = None
                    sj_vacancy_salary_currency = None

                else:
                    sj_vacancy_salary_currency = sj_vacancy_salary_status[-1]
                    sj_vacancy_salary = sj_vacancy_salary.split('—')
                    try:
                        sj_vacancy_salary_min = int(re.sub("\D", "", sj_vacancy_salary[0]))
                    except ValueError:
                        sj_vacancy_salary_min = None
                    try:
                        sj_vacancy_salary_max = int(re.sub("\D", "", sj_vacancy_salary[-1]))
                    except ValueError:
                        sj_vacancy_salary_max = None

            else:
                sj_vacancy_salary_min = None
                sj_vacancy_salary_max = None
                sj_vacancy_salary_currency = None

            sj_vacancy_data['name'] = sj_vacancy_name
            sj_vacancy_data['company'] = sj_vacancy_company
            sj_vacancy_data['city'] = sj_vacancy_city
            sj_vacancy_data['salary_min'] = sj_vacancy_salary_min
            sj_vacancy_data['salary_max'] = sj_vacancy_salary_max
            sj_vacancy_data['currency'] = sj_vacancy_salary_currency
            sj_vacancy_data['link'] = sj_vacancy_link
            sj_vacancy_data['site'] = 'sj.ru'

            vacancies_final_list.append(sj_vacancy_data)

        sj_page_count += 1

    sj_vacancies_count = len(vacancies_final_list) - hh_vacancies_count
    print(
        f'Было обработано {sj_page_count} страниц выдачи sj.ru. Была собрана информация о {sj_vacancies_count} вакансиях')

    return vacancies_final_list
