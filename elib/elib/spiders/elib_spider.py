# coding=utf8

from datetime import datetime
import urlparse
import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, Response
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

from elib.items import Book


class BookLoader(ItemLoader):

    format_map = {u"/images/adobe_icon.gif": "PDF",
                  u"/images/epubDRM_icon.gif": "EPUB",
                  u"/images/mobi_icon.gif": "MobiPocket"}

    default_item_class = Book
    default_output_processor = TakeFirst()
    
    #author_out = Identity()
    
    publish_date_in = MapCompose(lambda s: datetime.strptime(s, "%Y%m").date())

    format_in = MapCompose(lambda f: BookLoader.format_map[f])
    format_out = Join(",")


class ElibSpider(BaseSpider):
    name = "elib"
    allowed_domains = ["elib.se"]
    start_urls = [
        #"http://elib.se/library/dynamic_page.asp?page=O&lib=40"
        "http://www.elib.se/library/search.asp?title=&author=&isbn=&publisher=&lang=SE&typ50=50&typ58=58&lib=40&option=&secondrun=YES"
    ]

    field_map = {u"Titel": "title", u"Författare": "author",
                 u"Förlag": "publisher", u"Språk": "language",
                 u"Kategori": "category", u"Publiceringsdatum": "publish_date",
                 u"Beskrivning": "description", u"Format": "format"}

    def parse(self, response):
    
        selector = HtmlXPathSelector(response)
    
        # Parse next page
        next_url = selector.select(u"//a[text()='Nästa >>']/@href").extract()
        if len(next_url) > 0:
            yield Request(urlparse.urljoin(response.url, next_url[0]))
        
        # Parse all books
        for book_url in selector.select("//a[starts-with(@href, 'ebook_detail.asp') and ./img]/@href").extract():
            yield Request(urlparse.urljoin(response.url, book_url), callback=self.parse_book)

    def parse_book(self, response):

        isbn = re.findall("id_type=ISBN&id=([0-9xX]+)", response.url)[0]
        loader = BookLoader()
        loader.add_value("isbn", [isbn])

        rows = HtmlXPathSelector(response).select("//table[@class='MainTable']/tr")
        for row in rows:

            header = row.select(".//span[@class='BodytextHeadingTable']/text()").extract()
            data   = row.select(".//*[@class='Bodytext' or @class='BodytextBold' or @class='BodytextLink']")
            
            if len(header) == 1:
                header = header[0][:-1]
                value = map(lambda x: re.sub('<[^<]+?>', ' ', x).strip(), data.extract())
                if header in self.field_map:
                    if header == "Format":
                        value = data.select("img/@src").extract()
                    loader.add_value(self.field_map[header], value)
                if header == "ID":
                    loader.add_value("isbn_13", [re.findall("ISBN13:([0-9\-]+)", value[0])[0].replace("-", "")])
                    
        loader.add_value("cover", ["http://www.elib.se/product_images/ISBN" + isbn + ".jpg"])
        return loader.load_item()
            

