# coding=utf8

from scrapy.item import Item, Field

class Book(Item):
    isbn = Field()
    isbn_13 = Field()
    title = Field()
    author = Field()
    category = Field()
    publisher = Field()
    publish_date = Field()
    language = Field()
    format = Field()
    description = Field()
    cover = Field()

