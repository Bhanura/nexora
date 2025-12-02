import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.documents import Document

# 1. Load Secrets
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["nexora_db"]
collection = db["raw_materials"]

# 3. Setup Gemini Embeddings
# We use 'text-embedding-004' which matches our Index definition (768 dimensions)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def run_indexing():
    print("--- 1. Fetching Raw Data ---")
    # We find documents that DO NOT have an embedding yet
    raw_docs = list(collection.find({"embedding": {"$exists": False}}))
    print(f"Found {len(raw_docs)} documents to process.")

    if not raw_docs:
        print("Nothing new to index!")
        return

    # 4. Create LangChain Documents
    # We need to convert Mongo dicts into LangChain 'Document' objects
    documents_to_embed = []
    ids_to_update = []
    
    for doc in raw_docs:
        # We only want to embed the 'text_content'
        if "text_content" in doc and doc["text_content"]:
            # Create a Document object
            new_doc = Document(
                page_content=doc["text_content"],
                metadata={"source": doc.get("source_url", "unknown")}
            )
            documents_to_embed.append(new_doc)
            ids_to_update.append(doc["_id"])

    # 5. Generate Vectors & Save
    if documents_to_embed:
        print(f"--- 2. Generating Embeddings for {len(documents_to_embed)} docs ---")
        
        # This function automatically:
        # 1. Calls Gemini API
        # 2. Gets the vectors
        # 3. Saves them back to MongoDB Atlas in the 'embedding' field
        vector_store = MongoDBAtlasVectorSearch.from_documents(
            documents=documents_to_embed,
            embedding=embeddings,
            collection=collection,
            index_name="vector_index" # Must match the name you typed in Atlas UI
        )
        
        print("--- 3. Success! Data is now Vectorized ---")

if __name__ == "__main__":
    run_indexing()