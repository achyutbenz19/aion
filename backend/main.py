from time import sleep
from utils.chat_llm import ChatLLM
from utils.file_manager import FileManager
from utils.screenshot_comparator import ScreenshotComparator
from utils.vectorstore import Vectorstore
from utils.vision_llm import VisionLLM

chat_llm = ChatLLM()
file_manager = FileManager()
screenshot_comparator = ScreenshotComparator("./backend/archive")
vectorstore = Vectorstore()
vision_llm = VisionLLM()

if __name__ == "__main__":
    ss_taken = 0
    while True and ss_taken <= 1:
        sleep(5)
        path = screenshot_comparator.take_screenshot()
        result = screenshot_comparator.process_upload(path)
        print(result)
        
        if result == "Changes detected" or result == "No previous screenshot to compare":
            signed_url = file_manager.upload_file(path)
            summary = vision_llm.vision(signed_url)
            print(summary)
            metadata = { "file_url": signed_url }
            document = file_manager.get_docs(summary, metadata)
            vectorstore.add(document)
            
        ss_taken += 1