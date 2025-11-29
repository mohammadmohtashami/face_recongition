import yaml 
import os 
import cv2
import time
from pathlib import Path
from dotenv import load_dotenv
from face_detection import detect
from video_capture import stream_capture
from config import BASE_DIR , SOURCE
from utils.logger import logger 


Logger = logger ("main")

def run():
    
    streams = stream_capture(SOURCE)
    for stream in streams : 
        img = detect(stream)


        cv2.imshow("Frame" , img)
        Logger.info("camera streaming ....")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            Logger.info("camera streamin is stopping ... ")
            break
    
run()