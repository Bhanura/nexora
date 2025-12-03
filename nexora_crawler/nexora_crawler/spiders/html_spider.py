import scrapy
from nexora_crawler.items import NexoraCrawlerItem
from scrapy_playwright.page import PageMethod

class HtmlSpider(scrapy.Spider):
    name = "html_spider"
    
    def start_requests(self):
        # Let's crawl a documentation page (e.g., Scrapy's own tutorial)
        # or a simple text page.
        url = "https://quotes.toscrape.com/"
        
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True, 
            )
        )

    async def parse(self, response):
        # Extract text from specific elements (p, div, etc.)
        # We join them together to make one big block of text
        
        # This selector gets all text inside <span> tags with class "text"
        quotes = response.css('span.text::text').getall()
        
        full_text = "\n".join(quotes)
        
        # Create the item
        item = NexoraCrawlerItem()
        item['source_url'] = response.url
        item['text_content'] = full_text # <--- This is what the Indexer needs!
        
        yield item