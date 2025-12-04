import cv2
from pathlib import Path
from face_detection import detect , compiled_model , input_layer , process_results , draw_boxes
from video_capture import stream_capture
from config import BASE_DIR , SOURCE ,EXIST_MODEL , THRESHOLD
from utils.logger import logger 
import numpy as np 

Logger = logger ("main")

def run():
    
    streams = stream_capture(SOURCE)
    for stream in streams : 
        if EXIST_MODEL == False:
            img = detect(stream)


            cv2.imshow("Frame" , img)
            Logger.info("camera streaming ....")
            if cv2.waitKey(1) & 0xFF == ord("q"):
                Logger.info("camera streamin is stopping ... ")
                break
        else : 
            img = cv2.resize(stream, (640 ,640))
            frame = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32)/255.0
            frame = np.transpose(frame , (2,0,1))
            frame = np.expand_dims(frame , 0)
            result = compiled_model.infer({input_layer : frame})
            boxes =process_results(stream , result , thresh=THRESHOLD)
            final_result =draw_boxes(stream , boxes)
            cv2.imshow("Face detection" , final_result)
run()