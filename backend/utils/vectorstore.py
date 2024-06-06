import os
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

class Vectorstore:
    def __init__(self):
        self.client : Client = create_client(supabase_url, supabase_key)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = SupabaseVectorStore(self.client, self.embeddings, "aion_table")
        print("Initalized")
        
    def add(self, docs):
        self.vectorstore.add_documents(docs)
        print("Added")
    
    def query(self, question):
        return self.vectorstore.similarity_search(question)