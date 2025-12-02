import cv2
import os 
import time 

cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("the camera couldnt open ... ")
    exit()
    
os.makedirs("images" , exist_ok=True)


for i in range(150): 
        ret , frame = cap.read()
        if ret :           
            filename = f"images/{i}.jpg"
            cv2.imwrite(filename , frame)
            time.sleep(1)
cap.release()
print("the record 250 images have done !")
