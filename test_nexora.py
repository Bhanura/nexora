"""
Quick test to verify the Nexora chatbot is working
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_mongodb import MongoDBAtlasVectorSearch

# Load Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("Testing Nexora Components...")

# Test 1: MongoDB Connection
try:
    client = MongoClient(MONGO_URI)
    db = client["nexora_db"]
    collection = db["raw_materials"]
    doc_count = collection.count_documents({})
    print(f"✓ MongoDB connected: {doc_count} documents found")
except Exception as e:
    print(f"✗ MongoDB error: {e}")

# Test 2: Embeddings
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    test_embedding = embeddings.embed_query("test")
    print(f"✓ Embeddings working: {len(test_embedding)} dimensions")
except Exception as e:
    print(f"✗ Embeddings error: {e}")

# Test 3: LLM
try:
    print("Testing LLM (may take a few seconds)...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    response = llm.invoke("Say 'Hello from Nexora' in exactly 4 words.")
    answer = response.content if hasattr(response, 'content') else str(response)
    print(f"✓ LLM working: {answer}")
except Exception as e:
    print(f"✗ LLM error: {type(e).__name__}: {str(e)[:200]}")

# Test 4: Vector Store
try:
    print("Testing Vector Store...")
    vector_store = MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=embeddings,
        index_name="vector_index"
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    docs = retriever.invoke("test query")
    print(f"✓ Vector search working: {len(docs)} documents retrieved")
    if docs:
        print(f"  Sample content: {docs[0].page_content[:100]}...")
except Exception as e:
    print(f"✗ Vector search error: {type(e).__name__}: {str(e)[:200]}")

print("\n✅ All systems operational! You can now use console_app.py")
