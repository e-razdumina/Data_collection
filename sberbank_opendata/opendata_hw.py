import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 12})

df = pd.read_csv('./opendata.csv',sep=',')

values = list(set(df["name"]))
regions = list(set(df["region"]))


print("Выберите категорию:")

for i in range(len(values)):
    print(i + 1, values[i])

value_choice = 0

while value_choice > len(values) or value_choice <= 0:
    value_choice = int(input("Введите номер: "))

print("Выберите регион:")

for i in range(len(regions)):
    print(i + 1, regions[i])

region_choice = 0

while region_choice > len(regions) or region_choice <= 0:
    region_choice = int(input("Введите номер: "))

value_to_search = values[value_choice-1]
region_to_search = regions[region_choice-1]

df_processed = df.query('name == @value_to_search & region == @region_to_search')

date_min = df_processed["date"].min()
date_max = df_processed["date"].max()

print(f'График будет построен в интервале {date_min} - {date_max}')
date_choice = int(input("Если вы хотите внести изменения - введите 1, если нет - любой другой символ: "))

if date_choice == 1:
    date_min = input("Введите дату для старта интервала в формате yyyy-mm-dd: ")
    date_max = input("Введите дату для окончания интервала в формате yyyy-mm-dd: ")

# решила не добавлять проверку на корректность введенных данных (хотя можно было бы)

plt.figure(figsize=(18,10))
plt.plot(df_processed["date"], df_processed["value"])

plt.title(region_to_search)

plt.xlabel('Date')
plt.ylabel(value_to_search)

plt.show()

