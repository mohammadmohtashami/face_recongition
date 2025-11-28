import yaml 
import os 
from pathlib import Path
import logging
from dotenv import load_dotenv
from face_detection import detect
from video_capture import stream_capture
import cv2

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR , 'configs/config.yaml')
load_dotenv(dotenv_path=dotenv_path)
SOURCE =int(os.getenv("SOURCE" , 0))
FPS = os.getenv("FPS",10)
VIDEO_FLAG = os.getenv("VIDEO_FLAG",False)
SAVE_DATA = os.getenv("SAVE_DATA", False)
LOG_LEVEL =os.getenv("LOG_LEVEL" , 30)

logging.basicConfig(
    level = LOG_LEVEL ,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run():
    
    streams = stream_capture(SOURCE)
    for stream in streams : 
        img = detect(stream)
        cv2.imshow("Frame" , img)
        logging.info("camera streaming ....")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            logging.info("camera streamin is stopping ... ")
            break
    
run()