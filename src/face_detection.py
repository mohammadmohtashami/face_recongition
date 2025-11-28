import cv2 
import matplotlib.pyplot as plt 


face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

def  detect (img):
    gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_img , scaleFactor=1.1 , minNeighbors=5 , minSize=(40 , 40))
    for (x , y , w ,h ) in face : 
        cv2.rectangle(img ,(x,y), (x+w , y+h ), (0,255 , 0) , 4)
        
    return img