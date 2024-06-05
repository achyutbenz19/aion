import os
import open_clip
import numpy as np
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from PIL import Image

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
class Vectorstore:
    def __init__(self):
        open_clip.list_pretrained()
        self.model_name = "ViT-B-32"
        self.checkpoint = "laion2b_s34b_b79k"
        self.embeddings = OpenCLIPEmbeddings(model_name=self.model_name, checkpoint=self.checkpoint)
        self.client : Client = create_client(supabase_url, supabase_key)
        self.vectorstore = SupabaseVectorStore(self.client, self.embeddings, "aion_table")
        print("Initalized")
        
    def add(self, docs):
        self.vectorstore.add_documents(docs)
        print("Added")
    
    def query(self, question):
        return self.vectorstore.similarity_search(question)

v=Vectorstore()