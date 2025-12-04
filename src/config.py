import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR , 'configs/config.yaml')
load_dotenv(dotenv_path=dotenv_path)
SOURCE =int(os.getenv("SOURCE" , 0))
FPS = os.getenv("FPS",10)
VIDEO_FLAG = os.getenv("VIDEO_FLAG",False)
SAVE_DATA = os.getenv("SAVE_DATA", False)
LOG_LEVEL = int (os.getenv("LOG_LEVEL" , 30))
MODEL_PATH = os.getenv("MODEL_PATH")
EXIST_MODEL = int(os.getenv("EXIST_MODEL" , 0))
CLASSES = list(os.getenv("CLASSES", "FACE"))
IMAGE_SAVED_PATH = os.getenv("IMAGE_SAVED_PATH")
THRESHOLD = os.getenv("THRESHOLD" , 0.5)