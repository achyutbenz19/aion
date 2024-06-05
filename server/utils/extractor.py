import open_clip
import numpy as np
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from PIL import Image

class Extractor:
    def __init__(self, chunk_size=500, chunk_overlap=0):
        open_clip.list_pretrained()
        self.model_name = "ViT-B-32"
        self.checkpoint = "laion2b_s34b_b79k"
        self.embeddings = OpenCLIPEmbeddings(model_name=self.model_name, checkpoint=self.checkpoint)
    
    def get_embeddings(self, file):
        return self.embeddings.embed_image([file])