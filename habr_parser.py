from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import datetime


Article = namedtuple('Article', ('article_id', 'header', 'tags', 'text', 'public_datetime'))


def parse_article(article_id: int) -> Article:
    url = f'https://habr.com/ru/post/{article_id}/'

    response = requests.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.text)

    return Article(
        article_id,                                                                                               # article_id
        soup.find(name='h1').get_text(),                                                                          # header
        [tag.get_text().lower() for tag in soup.find_all(name='li', attrs={'class': 'tm-separated-list__item'})], # tags
        soup.find(name='div', attrs={'class': 'article-formatted-body'}).get_text(),                              # text
        datetime.datetime.strptime(soup.find(name='time').get('datetime'), '%Y-%m-%dT%H:%M:%S.000Z')              # public_datetime
    )

