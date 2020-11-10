# Task 1

import requests
import json
from pprint import pprint

main_link = 'https://api.github.com/users'
user_name = 'e-razdumina'

response = requests.get(f'{main_link}/{user_name}/repos')

data = response.json()
repos = []

for dict in data:
    repos.append(dict['name'])

answer = f'У пользователя {user_name} {len(repos)} публичных репозиториев на GitHub: {repos}'

print(answer)

with open('lesson-1.json', 'w') as f:
    f.write(answer)

# Task 2
import time
import hashlib

main_link = 'http://gateway.marvel.com/v1/public/comics'

apikey = '203a87f40d94203936a5d3f5908a0a4c'
private_key = '8b904e0796e42a659ea5fc07eb0b97bed06090e8'
ts = time.time()
str_for_hash = f'{ts}{private_key}{apikey}'
hash = hashlib.md5(str_for_hash.encode())

params = {
    'apikey': apikey,
    'ts': ts,
    'hash': hash
}

response = requests.get(main_link, params=params)

# Не получилось разобраться как сделать правильный хэш-ключ
# hash - a md5 digest of the ts parameter, your private key and your public key (e.g. md5(ts+privateKey+publicKey)
 

# data = response.json()
#
# pprint(data)
