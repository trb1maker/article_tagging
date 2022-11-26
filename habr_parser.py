from collections import namedtuple
from typing import Optional
from bs4 import BeautifulSoup
import requests
import datetime


def parse_view(view: str) -> int:
    k = 1
    
    if 'K' in view:
        k = 1_000
        view = view.replace('K', '')
    elif 'M' in view:
        k = 1_000_000
        view = view.replace('M', '')

    return int(float(view) * k)


Article = namedtuple('Article', ('id',
                                 'header',
                                 'tags',
                                 'text',
                                 'date',
                                 'rate',
                                 'view',
                                 'bookmark',
                                 'comment'))


def parse_article(id: int) -> Optional[Article]:
    url = f'https://habr.com/ru/post/{id}/'

    response = requests.get(url)

    if response.status_code == 200:
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

        return Article(
            id,
            header,
            tags,
            text,
            date,
            rate,
            view,
            bookmark,
            comment
        )

    else:
        return None


# Небольшая демонстрация
if __name__ == '__main__':

    first_article = 1

    article = parse_article(first_article)

    print(
        f'Самая первая статья на Хабре на тему {article.header} опубликована {article.date.strftime("%d.%m.%Y")}')
    print(f'\n{article.text}\n')
    print(article.tags)
