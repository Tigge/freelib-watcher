# coding=utf8

from scrapy.item import Item, Field

class Book(Item):
    title = Field()
    isbn = Field()
    isbn_13 = Field()
    author = Field()
    category = Field()
    publisher = Field()
    publish_date = Field()
    language = Field()
    format = Field()
    isbn = Field()
    description = Field()
    cover = Field()

