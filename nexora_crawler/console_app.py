import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_mongodb import MongoDBAtlasVectorSearch

# 1. Load Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Setup Database Connection
client = MongoClient(MONGO_URI)
db = client["nexora_db"]
collection = db["raw_materials"]

# 3. Setup Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# 4. Connect to the Vector Store
vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name="vector_index"
)

# 5. Setup the LLM (using gemini-2.5-flash - fast and reliable)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# 6. Create the Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

def start_chat():
    print("----------------------------------------------------------------")
    print("Welcome to Nexora")
    print("Type 'exit' to quit.")
    print("----------------------------------------------------------------")

    while True:
        query = input("\nUser: ")
        
        if query.lower() in ["exit", "quit"]:
            print("Nexora: Goodbye!")
            sys.exit()

        if not query.strip():
            continue

        print("Nexora: Thinking...", end="\r")

        try:
            # Get relevant documents
            source_docs = retriever.invoke(query)
            
            # Format context
            context = "\n\n".join(doc.page_content for doc in source_docs)
            
            # Create prompt
            prompt_text = f"""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {query}"""
            
            # Get response
            response = llm.invoke(prompt_text)
            answer = response.content if hasattr(response, 'content') else str(response)

            print(f"Nexora: {answer}                    ")  # Extra spaces to clear "Thinking..."
            
            # Print Sources
            if source_docs:
                unique_sources = {doc.metadata.get('source', 'Unknown') for doc in source_docs}
                print(f"\n[Sources: {', '.join(unique_sources)}]")
            else:
                print("\n[Source: General Knowledge]")

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    start_chat()