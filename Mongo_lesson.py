from vacancies_project import vacancies_pars
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancies']

vacancies_info = vacancies_pars()

db.vacancies.insert_many(vacancies_info)

salary_to_search = int(input('Введите зарплату для поиска: '))

# db.vacancies.find({'$or': [{'salary_min': {'$gte': salary_to_search}}, {'salary_max': {'$gte': salary_to_search}}]})
db.vacancies.find({})
