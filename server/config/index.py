import os
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
from langchain_community.vectorstores import SupabaseVectorStore

UPLOAD_FOLDER = './archive'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

CLIENT : Client = create_client(supabase_url, supabase_key)
EMBEDDINGS = OpenAIEmbeddings()
VECTORSTORE = SupabaseVectorStore(CLIENT, EMBEDDINGS, "aion_table")