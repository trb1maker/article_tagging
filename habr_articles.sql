BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "habr_articles" (
	"article_id"	INTEGER NOT NULL,
	"header"	TEXT,
	"tags"	TEXT,
	"text"	TEXT,
	"public_datetime"	TEXT,
	"rate"	TEXT,
	"view"	TEXT,
	"bookmark"	TEXT,
	"comment"	TEXT,
	"status"	TEXT NOT NULL,
	PRIMARY KEY("article_id")
);
COMMIT;
