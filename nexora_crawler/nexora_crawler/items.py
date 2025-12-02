import scrapy

class NexoraCrawlerItem(scrapy.Item):
    # This is where we store file URLs (like "http://site.com/doc.pdf")
    file_urls = scrapy.Field()
    
    # Scrapy will fill this in automatically when the file is downloaded
    files = scrapy.Field()
    
    # We will still keep a text field for normal page content
    text_content = scrapy.Field()
    source_url = scrapy.Field()
