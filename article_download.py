from collections import namedtuple
from typing import Optional

from bs4 import BeautifulSoup
import requests

import datetime
import random
import time
import csv


Article = namedtuple('Article', ('id', 'header', 'tags', 'text', 'date', 'rate', 'view', 'bookmark', 'comment'))


def parse_view(view: str) -> int:
    k = 1
    
    if 'K' in view:
        k = 1_000
        view = view.replace('K', '')
    elif 'M' in view:
        k = 1_000_000
        view = view.replace('M', '')

    return int(float(view) * k) 


def parse_article(id: int) -> Optional[Article]:
    url = f'https://habr.com/ru/post/{id}/'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, features='html.parser')

    header = soup.find(name='h1') \
                 .get_text()

    tags = [tag.get_text().lower() for tag in soup.find_all(
            name='li', attrs={'class': 'tm-separated-list__item'})]

    text = soup.find(name='div', attrs={'class': 'article-formatted-body'}) \
               .get_text()

    date = datetime.datetime.strptime(soup.find(name='time').get(
        'datetime'), '%Y-%m-%dT%H:%M:%S.000Z')

    rate = int(soup.find(name='span', attrs={'class': 'tm-votes-meter__value'})
                   .get_text()
                   .strip())

    view = parse_view(soup.find(name='span', attrs={'class': 'tm-icon-counter__value'})
                          .get_text()
                          .strip())

    bookmark = int(soup.find(name='span', attrs={'class': 'bookmarks-button__counter'})
                       .get_text()
                       .strip())

    try:
        # Если количество комментариев равно 0, то при парсинге число почему-то опускатеся.
        # Я не смог разобраться, почему так происходит и обернул это все в try / except

        comment = int(soup.find(name='span', attrs={'class': 'tm-article-comments-counter-link__value'})
                          .get_text()
                          .strip()
                          .split(' ')[1])
    except IndexError:
        comment = 0

    return Article(id, header, tags, text, date, rate, view, bookmark, comment)


def get_articles(start_id: int):
    stop_id = start_id + 10_000

    file_name = f'data_{stop_id}.csv'

    with open(file_name, 'w') as f:
        w = csv.writer(f)

        for id in range(start_id, stop_id):
            article = parse_article(id)

            if article:
                w.writerow(article)
            
            time.sleep(random.randint(1, 3) * 0.3)


if __name__ == '__main__':
    start_id = 1

    while start_id <= 700_000:
        print(f'Скачиваю и сохранаяю данные {start_id} - {start_id + 10_000}')
        
        get_articles(start_id)
        
        time.sleep(60)
        start_id += 10_000
