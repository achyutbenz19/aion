import time
import os
from utils.screenshot_comparator import ScreenshotComparator
from config.index import UPLOAD_FOLDER

def test_screenshot_comparator():
    comparator = ScreenshotComparator(UPLOAD_FOLDER, threshold=10)

    try:
        while True:
            filename = f'screenshot_{int(time.time())}.png'
            current_screenshot_path = comparator.take_screenshot(filename)

            if comparator.previous_screenshot_path:
                result = comparator.compare_screenshots(comparator.previous_screenshot_path, current_screenshot_path)
                print(result)

                if result == "Similar":
                    os.remove(current_screenshot_path)
                    current_screenshot_path = comparator.previous_screenshot_path

            comparator.previous_screenshot_path = current_screenshot_path

            time.sleep(5)
    except KeyboardInterrupt:
        print("Screenshot capture stopped.")

if __name__ == "__main__":
    test_screenshot_comparator()
