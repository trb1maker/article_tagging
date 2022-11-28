from bs4 import BeautifulSoup
import requests

import datetime

import time

import csv


def parse_view(view: str) -> int:
    k = 1
    
    if 'K' in view:
        k = 1_000
        view = view.replace('K', '')
    elif 'M' in view:
        k = 1_000_000
        view = view.replace('M', '')

    return int(float(view) * k) 


def get_article(id: int) -> tuple:
    url = f'https://habr.com/ru/post/{id}/'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, features='html.parser')

    header = soup.find(name='h1') \
                 .get_text()

    tags = [tag.get_text().lower().strip() for tag in soup.find_all(name='li', attrs={'class': 'tm-separated-list__item'})]

    text = soup.find(name='div', attrs={'class': 'article-formatted-body'}) \
               .get_text()

    
    date = soup.find(name='time').get('datetime')
    
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    except:
        # Если формат даты неожиданный, сохраню исходные данные        
        pass

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
        comment = int(soup.find(name='span', attrs={'class': 'tm-article-comments-counter-link__value'})
                          .get_text()
                          .strip()
                          .split(' ')[1])
    except IndexError:
        # Если количество комментариев равно 0, то при парсинге число почему-то опускатеся.
        # Я не смог разобраться, почему так происходит и обернул это все в try / except
        comment = 0

    return (id, header, tags, text, date, rate, view, bookmark, comment)


def get_articles_batch(last_id: int, batch=10_000) -> int:
    start_id = last_id
    stop_id = last_id - batch

    file_name = f"data_{datetime.datetime.now().strftime('%Y-%m-%d')}_{last_id}.csv"

    with open(file_name, 'w') as f:
        w = csv.writer(f)

        for id in range(start_id, stop_id, -1):
            try:
                article = get_article(id)
                
                if article:
                    w.writerow(article)
            except:
                print(f'Ошибка парсинга статьи {id}')
            
            time.sleep(0.5)
    
    return stop_id


if __name__ == '__main__':
    last_id = 701_600 # ID последней статьи, опубликованной 2022-11-26

    while True:
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d [%H:%M]')}\t{last_id}")
        
        last_id = get_articles_batch(last_id)
        time.sleep(60 * 5)

