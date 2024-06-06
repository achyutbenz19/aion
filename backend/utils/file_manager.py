import os
from langchain.schema import Document
from config.index import CLIENT

class FileManager:
    def __init__(self):
        self.client = CLIENT
        self.bucket_name = "aion"
        self.storage = self.client.storage
    
    def create_bucket(self):
        try:
            existing_buckets = self.storage.list_buckets()
            if self.bucket_name not in [bucket['name'] for bucket in existing_buckets]:
                self.storage.create_bucket(self.bucket_name)
                print("Bucket created successfully.")
            else:
                print("Bucket already exists.")
        except Exception as e:
            print(f"Error creating bucket: {e}")
    
    def retrieve_buckets(self):
        try:
            buckets = self.storage.list_buckets()
            print(f"Available buckets: {buckets}")
            return buckets
        except Exception as e:
            print(f"Error retrieving buckets: {e}")
    
    def upload_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                print(f"File {filepath} does not exist.")
                return
            with open(filepath, 'rb') as f:
                self.storage.from_(self.bucket_name).upload(file=f, path=os.path.basename(filepath), file_options={"content-type": "image/jpg"})
                print(f"File {filepath} uploaded successfully.")
            return self.get_signed_url(os.path.basename(filepath))
        except Exception as e:
            print(f"Error uploading file: {e}")
    
    def get_signed_url(self, filename):
        try:
            response = self.storage.from_(self.bucket_name).create_signed_url(filename, 63072000)  # 2 years
            url = response['signedURL']
            return url
        except Exception as e:
            print(f"Error retrieving signed URL: {e}")
            return None        
    
    def get_docs(self, text, metadata):
        docs = [Document(page_content=text, metadata=metadata)] 
        return docs
