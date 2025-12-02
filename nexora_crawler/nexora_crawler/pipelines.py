import pymongo
import fitz # PyMuPDF
import os
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NexoraCrawlerPipeline:
    def process_item(self, item, spider):
        return item

class PdfParsingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check if the item has downloaded files
        if adapter.get('files'):
            # Get the path where Scrapy saved the file
            # 'files' is a list of dicts. We take the first one.
            file_info = adapter['files'][0] 
            relative_path = file_info['path']
            
            # Construct absolute path (files are in 'downloads' folder)
            # We assume current working directory is the project root
            absolute_path = os.path.join(os.getcwd(), 'downloads', relative_path)
            
            # Extract text
            extracted_text = self.extract_text_from_pdf(absolute_path)
            
            # Save the text back into the item
            adapter['text_content'] = extracted_text
            
        return item

    def extract_text_from_pdf(self, path):
        try:
            doc = fitz.open(path)
            text = []
            for page in doc:
                text.append(page.get_text())
            return "\n".join(text)
        except Exception as e:
            return f"Error reading PDF: {e}"
                
class MongoPipeline:
    def __init__(self):
        # We read the URI from the environment variable (loaded in settings.py)
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = "nexora_db"
        self.collection_name = "raw_materials" # We call it raw because it's not vectorized yet

    def open_spider(self, spider):
        # Connect when the spider starts
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        # Disconnect when finished
        self.client.close()

    def process_item(self, item, spider):
        # We convert the Scrapy Item to a normal Python Dictionary
        data = dict(item)
        
        # Insert into MongoDB
        self.db[self.collection_name].insert_one(data)
        
        return item