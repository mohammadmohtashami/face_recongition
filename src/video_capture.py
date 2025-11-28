import cv2 
import logging 

def stream_capture(SOURCE):
    cap = cv2.VideoCapture(SOURCE)
    
    if not cap.isOpened():
        logging.error("Camera cannot be opened")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to grab frame")
                break
                
            yield frame 
            
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Camera resources released")





