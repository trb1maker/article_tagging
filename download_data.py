from habr_parser import parse_article
import clickhouse_connect
import random
import time
import sys
import csv


if len(sys.argv) == 2 and sys.argv[1] == 'create':
    with clickhouse_connect.get_client(database='article') as db:
        SQL = '''
            CREATE TABLE habr_articles (
                id       UInt32,
                header   String,
                tags     Array(String),
                text     String,
                date     DateTime(),
                rate     Int8,
                view     UInt16,
                bookmark UInt8,
                comment  UInt16
            )

            ENGINE = MergeTree()
            PRIMARY KEY(id)
            '''

        db.query(query=SQL)


if len(sys.argv) == 4 and sys.argv[1] == 'download':
    start_id = int(sys.argv[2])
    stop_id = int(sys.argv[3])

    file_name = f'data_{start_id}.csv'

    with open(file_name, 'w') as f:
        w = csv.writer(f)

        for id in range(start_id, stop_id + 1):
            a = parse_article(id)

            if a:
                w.writerow(a)
            
            time.sleep(random.randint(1, 3) * 0.3)
