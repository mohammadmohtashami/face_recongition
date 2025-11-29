import cv2 
import matplotlib.pyplot as plt 
import datetime
from config import BASE_DIR
import os 

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

image_dir = os.path.join(BASE_DIR , "images")
os.makedirs(image_dir , exist_ok=True) 

def  detect (img):
    gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_img , scaleFactor=1.1 , minNeighbors=5 , minSize=(40 , 40))
    if len(face) > 0 :
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(image_dir , now)
        cv2.imwrite(f"{image_path}.jpg" , img)
    for (x , y , w ,h ) in face : 
        cv2.rectangle(img ,(x,y), (x+w , y+h ), (0,255 , 0) , 4)
        cv2.putText(img , text=f"Faces detected : {len(face)}", org =(20 ,20 ) ,color=(0,255,0) , fontFace=  cv2.FONT_HERSHEY_SIMPLEX , fontScale=0.8
)
    return img