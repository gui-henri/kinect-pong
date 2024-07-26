import cv2
from cv2.typing import MatLike
import sys

class WebCam:
    def __init__(self, webcam_index: int = 0) -> None:
        cv2.setLogLevel(0)
        self.cap = cv2.VideoCapture(webcam_index)
        self.is_opened = self.cap.isOpened()
        if not self.is_opened:
            print("Error: Could not open webcam.")

    def read(self) -> MatLike:
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture image")
            sys.exit(1)
        frame.flags.writeable = False
        return frame

    def cvt_color(self, frame: MatLike) -> MatLike:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    def release(self) -> None:
        self.cap.release()
        cv2.destroyAllWindows()