import cv2 
from utils.logger import logger

Logger = logger("video_capture")

def stream_capture(SOURCE):
    cap = cv2.VideoCapture(SOURCE)
    
    if not cap.isOpened():
        Logger.error("Camera cannot be opened")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                Logger.error("Failed to grab frame")
                break
                
            yield frame 
            
    finally:
        cap.release()
        cv2.destroyAllWindows()
        Logger.info("Camera resources released")





