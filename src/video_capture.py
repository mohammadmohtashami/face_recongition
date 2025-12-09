import cv2 
from .utils.logger import logger
import time 

Logger = logger("video_capture")

def stream_capture(SOURCE):
    cap = cv2.VideoCapture(SOURCE)
    
    if not cap.isOpened():
        Logger.error("Camera cannot be opened")
        return
    
    try:
        prev_frame_time = 0
        new_frame_time = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                Logger.error("Failed to grab frame")
                break
            new_frame_time = time.time()
            fps = 1/(new_frame_time - prev_frame_time)
            FPS = str(int(fps))
            cv2.putText(frame  , f'FPS : {FPS}'  , (7,70) , cv2.FONT_HERSHEY_SIMPLEX , fontScale=0.8 , color=(100 , 255,0))
            prev_frame_time = new_frame_time
            yield frame 
            
                
    finally:
        cap.release()
        cv2.destroyAllWindows()
        Logger.info("Camera resources released")





