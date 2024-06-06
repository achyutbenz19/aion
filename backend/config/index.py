import os
from supabase.client import Client, create_client

UPLOAD_FOLDER = './archive'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

CLIENT: Client = create_client(supabase_url, supabase_key)