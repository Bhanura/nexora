import scrapy
from nexora_crawler.items import NexoraCrawlerItem

class MediaSpider(scrapy.Spider):
    name = "media_spider"
    
    def start_requests(self):
        # A test URL with a dummy PDF file
        urls = [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # We create an Item to tell Scrapy "Download this!"
        item = NexoraCrawlerItem()
        
        # We give it the URL of the file we found
        item['file_urls'] = [response.url]
        item['source_url'] = response.url
        
        yield item