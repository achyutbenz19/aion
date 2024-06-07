from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from time import sleep
from utils.chat_llm import ChatLLM
from utils.file_manager import FileManager
from utils.screenshot_comparator import ScreenshotComparator
from utils.vectorstore import Vectorstore
from utils.vision_llm import VisionLLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_llm = ChatLLM()
file_manager = FileManager()
screenshot_comparator = ScreenshotComparator("./backend/archive")
vectorstore = Vectorstore()
vision_llm = VisionLLM()

@app.get("/")
def root():
    """
    Root endpoint to check if the API is live.
    """
    return {"aion": "live"}

@app.post("/start")
def start():
    """
    Endpoint to start the screenshot comparison process.
    Takes screenshots at intervals, processes them, and stores the results.
    """
    try:
        ss_taken = 0
        while ss_taken <= 1:
            sleep(5)
            path = screenshot_comparator.take_screenshot()
            result = screenshot_comparator.process_upload(path)
            print(result)
            
            if result == "Changes detected" or result == "No previous screenshot to compare":
                ss_taken += 1
                signed_url = file_manager.upload_file(path)
                summary = vision_llm.vision(signed_url)
                print(summary)
                metadata = {"file_url": signed_url}
                document = file_manager.get_docs(summary, metadata)
                vectorstore.add(document)
                
        return {"status": "Processing completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatQuery(BaseModel):
    query: str

@app.post("/chat")
def chat(query: ChatQuery):
    """
    Endpoint to handle chat queries.
    
    Args:
    query (ChatQuery): The user's query string wrapped in a Pydantic model.
    
    Returns:
    dict: The response generated by the chat LLM.
    """
    try:
        docs = vectorstore.query(query.query)
        docs = file_manager.format_docs(docs)
        response = chat_llm.chat(query.query, docs)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
