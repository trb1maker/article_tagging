from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import datetime


Article = namedtuple('Article', ('article_id',
                                 'header',
                                 'tags',
                                 'text',
                                 'public_datetime',
                                 'rate',
                                 'view',
                                 'bookmark',
                                 'comment',
                                 'status'))

# Для создания Article нужны article_id, status
# и еще _EmptyCount параметров.
_EmptyCount = 8


def parse_article(article_id: int) -> Article:
    url = f'https://habr.com/ru/post/{article_id}/'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')

        return Article(

            # article_id
            article_id,

            # header
            soup.find(name='h1') \
                .get_text(),

            # tags
            [tag.get_text().lower() for tag in soup.find_all(
                name='li', attrs={'class': 'tm-separated-list__item'})],

            # text
            soup.find(name='div', attrs={'class': 'article-formatted-body'}) \
                .get_text(),

            # public_datetime
            datetime.datetime.strptime(soup.find(name='time').get(
                'datetime'), '%Y-%m-%dT%H:%M:%S.000Z'),

            # rate
            soup.find(name='span', attrs={'class': 'tm-votes-meter__value'}) \
                .get_text()\
                .strip(),

            # view
            soup.find(name='span', attrs={'class': 'tm-icon-counter__value'}) \
                .get_text() \
                .strip(),

            # bookmark
            soup.find(name='span', attrs={'class': 'bookmarks-button__counter'}) \
                .get_text() \
                .strip(),

            # comment
            soup.find(name='span', attrs={'class': 'tm-article-comments-counter-link__value'}) \
                .get_text() \
                .strip() \
                .split(' ')[1],

            # status
            'ok'
        )

    elif response.status_code == 404:
        return Article(article_id, *(None for _ in range(_EmptyCount)), 'deleted')
    elif response.status_code == 403:
        return Article(article_id, *(None for _ in range(_EmptyCount)), 'hidden')

    else:
        raise Exception(f'Ошибка сервера: {response.status_code}')
