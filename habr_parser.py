from collections import namedtuple
from bs4 import BeautifulSoup
import requests

Article = namedtuple('Article', ('article_id', 'header', 'tags', 'text'))


def parse_article(article_id: int) -> Article:
    url = f'https://habr.com/ru/post/{article_id}/'

    response = requests.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.text)

    header = soup.find(name='h1') \
                 .get_text()

    tags = [tag.get_text().lower() for tag in soup.find_all(name='li', attrs={'class': 'tm-separated-list__item'})]

    text = soup.find(name='div', attrs={'class': 'article-formatted-body'}) \
               .get_text()

    return Article(article_id, header, tags, text)
