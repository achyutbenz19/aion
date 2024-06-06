from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from config.index import CLIENT

class Vectorstore:
    def __init__(self):
        self.client = CLIENT
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = SupabaseVectorStore(self.client, self.embeddings, "aion_table")
        print("Initalized")
        
    def add(self, docs):
        self.vectorstore.add_documents(docs)
        print("Added")
    
    def query(self, question):
        return self.vectorstore.similarity_search(question)
