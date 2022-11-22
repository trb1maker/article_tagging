from habr_parser import parse_article
import sqlite3
import random
import time

first_article = 2
last_article = 100

with sqlite3.connect('habr_articles.db') as db:

    SQL = 'INSERT INTO habr_articles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    
    for article_id in range(first_article, last_article + 1):
        try:
            article = parse_article(article_id)
        
        except Exception as e:
            print(e)

            if input('Продолжить выполнение цикла? (y): ') != 'y':
                break
        
        db.execute(SQL, (article.article_id,
                         article.header,
                         ','.join(article.tags) if article.tags else None,
                         article.text,
                         article.public_datetime.strftime('%Y-%m-%d %H:%M:%S') if article.public_datetime else None,
                         article.rate,
                         article.view,
                         article.bookmark,
                         article.comment,
                         article.status))
        
        db.commit()

        time.sleep(random.randint(1, 3))
