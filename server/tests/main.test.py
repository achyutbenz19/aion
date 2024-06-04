import os
import time
from utils.screenshot_comparator import ScreenshotComparator
from config.index import UPLOAD_FOLDER

def test_screenshot_processor():
    processor = ScreenshotComparator('./archive', threshold=10)
    try:
        while True:
            current_screenshot_path = os.path.join(processor.archive_folder, f'screenshot_{int(time.time())}.png')

            processor.take_screenshot(current_screenshot_path)

            if processor.previous_screenshot_path:
                result = processor.compare_screenshots(processor.previous_screenshot_path, current_screenshot_path)
                print(result)

                if result == "Similar":
                    os.remove(current_screenshot_path)
                    current_screenshot_path = processor.previous_screenshot_path 

            processor.previous_screenshot_path = current_screenshot_path
            time.sleep(5)
    except KeyboardInterrupt:
        print("Screenshot capture stopped.")
        
test_screenshot_processor()