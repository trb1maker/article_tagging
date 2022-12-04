CREATE TABLE IF NOT EXISTS articles (
    article_id UInt32,
    date       DateTime,
    rate       Int16,
    views      UInt32,
    bookmarks  UInt32,
    comments   UInt32,
    header     String,
    tags       Array(String),
    text       String
)

ENGINE = MergeTree()
PRIMARY KEY article_id