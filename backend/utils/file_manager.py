import os
from langchain.schema import Document

class FileManager:
    def __init__(self):
        pass
    
    def get_docs(self, text, metadata):
        docs = [Document(page_content=text, metadata=metadata)] 
        return docs
