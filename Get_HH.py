# -*- coding: utf-8 -*-

"""
Примеры сложных запросов:

Трактористы на С/Х технику
job_title = [
    "NAME:((((Водитель OR Оператор) AND (Трактора OR Комбаина)) OR !Тракторист OR !Механизатор OR !Комбайнер) NOT Дворник) AND DESCRIPTION:(Сельхоз OR зерно OR Урожай OR Сельское OR Агро* OR посев NOT дворник)"]


Логист (Грузовые автоперевозки)
job_title = [
    "NAME:((логист* OR ((менеджер OR специалист) and ((транспортная AND документация) OR перевозки))) NOT продаж, NOT помощник, NOT стажёр, NOT руководитель, NOT поддержка, NOT морск*, NOT железнод*, NOT ЖД, NOT авиа*, NOT Мультимод*) AND DESCRIPTION:(NOT железнод*, NOT авиа*, NOT мультимод*, NOT морск*, NOT ЖД)"]


Специалист по охране труда (И вариации названия) - поиск только по названию
job_title = [
    "(!Специалист OR !Инженер) AND ((Охрана AND Труд) OR ((Пожар* OR Промышл* OR Техник*) AND Безопас*) OR (Чрезвычайные AND Ситуации) OR !ГОиЧС OR !ПБ OR !ТБ) NOT стажёр, NOT младший, NOT руководитель, NOT ведущий, NOT главный, NOT обслуживанию, NOT установка, NOT систем"]


Автослесари
NAME:((Жестянщик OR слесарь OR Кузовщик) NOT наладчик, NOT сборщик, NOT КИПиА, NOT Монтажник, NOT Маляр, NOT сборщик, NOT ученик, NOT стажёр, NOT начинающий, NOT электр*, NOT газ*, NOT оборуд*, NOT аварий*) AND DESCRIPTION:((Автомобилей OR Трактор OR С/Х OR Сель*) NOT стройка, NOT сантех*, NOT цех)


"""

import requests
import json
import time
import os
import shutil

# Переменные

"""Параметры дат задаются диапазонами, в связи с тем,
что объем выдачи по умолчанию ограничен 2000
Пары дат задаются двумя списками, соответственно:
    Первый элемент (FROM) + Первый элемент (TO)

Рекомендуется задать от 2-3 пар дат с интервалом в 10 дней
(При желании, можно уменьшить или увеличить шаг или ограничиться одной парой):
Пример:
    (FROM Сегодня - 30 дней + TO Сегодня - 20 дней);
    (FROM СЕГОДНЯ - 20 дней + TO Сегодня - 10 дней) и т.д.

Метод принимает только даты в формате ISO-8601, строкой"""

# Список дат ДО (Параметры запроса)
to_date_list = ['2024-02-15', '2024-03-04', '2024-03-16']

# Список дат ОТ (Параметры запроса)
from_date_list = ['2024-01-01', '2024-02-15', '2024-03-04']

# Поисковый запрос (Подробнее: https://kazan.hh.ru/article/1175)
job_title = [
    "NAME:(!Сварщик NOT сантех*, NOT водопровод*) and DESCRIPTION:(NOT авари*, NOT водопровод, NOT труб*)"]

counter = 0


# Запрос к API, забираем результаты поисковой выдачи

def getVac(p=0):
    # Не рекомендуется менять параметры поискового запроса
    # Подробная ифнормация о методе: https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies
    par = {'text': job_title,
           'area': '113',
           'search_field': 'name',
           'only_with_salary': 'true',
           'currency': 'RUR',
           'date_from': from_date,
           'date_to': to_date,
           'per_page': 50,
           'page': p}

    req = requests.get('https://api.hh.ru/vacancies', par)
    data = req.content.decode()
    req.close()
    return data


# Создать папки для ответов
shutil.rmtree('vac_list', ignore_errors=True)
shutil.rmtree('vac_desc', ignore_errors=True)

os.makedirs('vac_list', exist_ok=True)
os.makedirs('vac_desc', exist_ok=True)

# Собираем и записываем в Json доступные страницы

for from_date, to_date in zip(from_date_list, to_date_list):
    print(f'От - {from_date}\nДо - {to_date}\n')

    for page in range(0, 40):
        res = json.loads(getVac(page))
        nextChunkName = './vac_list/{}.json'.format(len(os.listdir('./vac_list')))
        chunk = open(nextChunkName, mode='w', encoding='utf8')
        chunk.write(json.dumps(res, ensure_ascii=False))
        chunk.close()
        if (res['pages'] - page) <= 1:
            break
        time.sleep(5)
        print(f'Собрано: {page+1} страниц')

print(len(os.listdir('./vac_list')), 'страниц собрано\n\n')
time.sleep(120)

# Забираем полное описание вакансий

print('Извлечение вакансий: \n\n')
for chunk in os.listdir('./vac_list'):
    f = open('./vac_list/{}'.format(chunk), encoding='utf8')
    cont = f.read()
    f.close()
    res = json.loads(cont)
    for vac in res['items']:
        req = requests.get(vac['url'])
        data = req.content.decode()
        req.close()
        fName = './vac_desc/{}.json'.format(vac['id'])
        f = open(fName, mode='w', encoding='utf8')
        f.write(data)
        f.close()
        time.sleep(1)
    counter += 1
    print(f'Готово: {counter} страниц')
    time.sleep(20)
print('Вакансии собраны')
