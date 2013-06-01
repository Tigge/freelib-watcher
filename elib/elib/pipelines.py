# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3

from scrapy.exceptions import DropItem

class SQLitePipeline(object):

    def __init__(self):
        self.db = sqlite3.connect('books.db')
        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, " +
                            "isbn13 TEXT, title TEXT, author TEXT, " +
                            "category TEXT, publisher TEXT, " +
                            "publish_date TEXT, language TEXT, format TEXT, " +
                            "description TEXT, cover TEXT, added TEXT)")
        self.db.commit()

    def book_to_tuple(self, book):
        return (book["isbn"], book["isbn_13"], book["title"],
                book["author"], book["category"], book["publisher"],
                book["publish_date"].isoformat(), book["language"],
                book["format"], book["description"], book["cover"])

    def process_item(self, book, spider):
        try:
            self.cursor.execute("INSERT INTO books VALUES(?, ?, ?, ?, ?, " + 
                                "?, date(?), ?, ?, ?, ?, datetime('now'))",
                                self.book_to_tuple(book))
            return book
        except sqlite3.IntegrityError:
            raise DropItem("Book already exists %s" % book)

    def close_spider(self, spider):
        self.db.commit()
