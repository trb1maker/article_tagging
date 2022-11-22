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

        header = soup.find(name='h1') \
                     .get_text()

        tags = [tag.get_text().lower() for tag in soup.find_all(
                name='li', attrs={'class': 'tm-separated-list__item'})]

        text = soup.find(name='div', attrs={'class': 'article-formatted-body'}) \
                   .get_text()

        public_datetime = datetime.datetime.strptime(soup.find(name='time').get(
            'datetime'), '%Y-%m-%dT%H:%M:%S.000Z')

        rate = soup.find(name='span', attrs={'class': 'tm-votes-meter__value'}) \
                   .get_text()\
                   .strip()

        view = soup.find(name='span', attrs={'class': 'tm-icon-counter__value'}) \
                   .get_text() \
                   .strip()

        bookmark = soup.find(name='span', attrs={'class': 'bookmarks-button__counter'}) \
                       .get_text() \
                       .strip()

        try:
            # Если количество комментариев равно 0, то при парсинге число почему-то опускатеся.
            # Я не смог разобраться, почему так происходит и обернул это все в try / except
            
            comment = soup.find(name='span', attrs={'class': 'tm-article-comments-counter-link__value'}) \
                          .get_text() \
                          .strip() \
                          .split(' ')[1]
        except IndexError:
            comment = '0'

        status = 'ok'

        return Article(
            article_id,
            header,
            tags,
            text,
            public_datetime,
            rate,
            view,
            bookmark,
            comment,
            status
        )

    elif response.status_code == 404:
        return Article(article_id, *(None for _ in range(_EmptyCount)), 'deleted')
    elif response.status_code == 403:
        return Article(article_id, *(None for _ in range(_EmptyCount)), 'hidden')

    else:
        raise Exception(f'Ошибка сервера: {response.status_code}')


# Небольшая демонстрация
if __name__ == '__main__':
    
    first_article = 1
    
    article = parse_article(first_article)

    print(f'Самая первая статья на Хабре на тему {article.header} опубликована {article.public_datetime.strftime("%d.%m.%Y")}')
    print(f'\n{article.text}\n')
    print(article.tags)
