import cv2 
import matplotlib.pyplot as plt 
import datetime
from config import BASE_DIR
import os 
import uuid 
from database.insertation import insertation

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

image_dir = os.path.join(BASE_DIR , "images")
os.makedirs(image_dir , exist_ok=True) 

def  detect (img):
    faces_uuid =[]
    gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_img , scaleFactor=1.1 , minNeighbors=5 , minSize=(40 , 40))

    for person in faces :
        name = "person" 
        face_uuid = str(uuid.uuid4())
        insertation(name,datetime.datetime.now() , face_uuid)

    if len(faces) > 0 and (face_uuid not in faces_uuid):
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(image_dir , now)
        cv2.imwrite(f"{image_path}.jpg" , img)
        faces_uuid.append(face_uuid)
        
    for (x , y , w ,h ) in faces : 
        cv2.rectangle(img ,(x,y), (x+w , y+h ), (0,255 , 0) , 4)
        cv2.putText(img , text=f"Faces detected : {len(faces)}", org =(20 ,20 ) ,color=(0,255,0) , fontFace=  cv2.FONT_HERSHEY_SIMPLEX , fontScale=0.8
)
    return img