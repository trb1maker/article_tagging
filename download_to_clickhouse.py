from habr_parser import parse_article
import clickhouse_connect
import random
import time


with clickhouse_connect.get_client(database='article') as db:
    # create_table_sql = '''
    #     CREATE TABLE habr_articles (
    #         id       UInt32,
    #         header   String,
    #         tags     Array(String),
    #         text     String,
    #         date     DateTime(),
    #         rate     Int8,
    #         view     UInt16,
    #         bookmark UInt8,
    #         comment  UInt16
    #     )

    #     ENGINE = MergeTree()
    #     PRIMARY KEY(id);

    #     '''

    # db.query(query=create_table_sql)

    last_id = db.query(query='select max(id) from habr_articles').result_set[0][0]

    current_id = last_id + 1
    stop_id = current_id + 1000
    
    error_limit = 10
    
    data = []
    
    while current_id <= stop_id and error_limit > 0:
        a = parse_article(current_id)

        if a:
            data.append(a)
            error_limit = 10
        else:
            error_limit -= 1
        
        time.sleep(random.randint(1, 3) * 0.3)
                
        print(f'{current_id}/{stop_id}')
        
        current_id += 1    
    
    db.insert(table='habr_articles',
              column_names=('id', 'header', 'tags', 'text', 'date', 'rate', 'view', 'bookmark', 'comment'),
              data=data)
