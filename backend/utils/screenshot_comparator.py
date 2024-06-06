import os
import time
import cv2
import pyautogui
import numpy as np
from config.index import ALLOWED_EXTENSIONS

class ScreenshotComparator:
    def __init__(self, archive_folder, threshold=10):
        self.archive_folder = archive_folder
        self.threshold = threshold
        self.previous_screenshot_path = None

        os.makedirs(self.archive_folder, exist_ok=True)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def compare_screenshots(self, screenshot1_path, screenshot2_path):
        screenshot1 = cv2.imread(screenshot1_path)
        screenshot2 = cv2.imread(screenshot2_path)

        if screenshot1.shape != screenshot2.shape:
            raise ValueError("Images must be of the same size")

        gray1 = cv2.cvtColor(screenshot1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(screenshot2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)

        diff_percentage = (np.sum(diff > 50) / diff.size) * 100

        if diff_percentage > self.threshold:
            return "Changes detected"
        else:
            return "Similar"

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            filename = f'screenshot_{int(time.time())}.png'
            file_path = os.path.join(self.archive_folder, filename)
            file.save(file_path)
            return file_path
        return None

    def take_screenshot(self, filename=None):
        if filename is None:
            filename = f'screenshot_{int(time.time())}.png'
        save_path = os.path.join(self.archive_folder, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return save_path

    def process_upload(self, current_screenshot_path):
        if not current_screenshot_path:
            return "Invalid file format", 400

        result = "No previous screenshot to compare"
        if self.previous_screenshot_path:
            result = self.compare_screenshots(self.previous_screenshot_path, current_screenshot_path)

            if result == "Similar":
                os.remove(current_screenshot_path)
                current_screenshot_path = self.previous_screenshot_path

        self.previous_screenshot_path = current_screenshot_path

        return result
