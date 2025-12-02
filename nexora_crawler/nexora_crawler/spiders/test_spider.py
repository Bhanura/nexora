import scrapy
import os
from scrapy_playwright.page import PageMethod

class TestSpider(scrapy.Spider):
    name = "test_spider"

    def start_requests(self):
        # TEST: Print a variable from .env (Check your console logs when running)
        print(f"Checking .env: API Key placeholder is -> {os.getenv('GOOGLE_API_KEY')}")

        # We target a specific URL
        url = "https://quotes.toscrape.com/js/" 
        
        # We tell Scrapy to use Playwright for this request
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True, 
            )
        )

    async def parse(self, response):
        # This function runs when the website data is downloaded.
        
        # Let's extract all the quote texts to verify it worked.
        # This CSS selector finds elements with class "text"
        for quote in response.css('span.text::text'):
            yield {
                'quote': quote.get()
            }