from config.index import VECTORSTORE ,CLIENT, EMBEDDINGS

class Vectorstore:
    def __init__(self):
        self.vectorstore = VECTORSTORE
        self.client = CLIENT
        self.embeddings = EMBEDDINGS
        print("Initalized")
        
    def add(self, docs):
        self.vectorstore.add_documents(docs)
        print("Added")
    
    def query(self, question):
        return self.vectorstore.similarity_search(question)

v = Vectorstore()