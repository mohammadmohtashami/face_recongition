import cv2 
from main import SOURCE
import logging 



cap = cv2.VideoCapture(int(SOURCE))


if cap.isOpened()== False:
    logging.error("cap can not open ")
    
while cap : 
    ret , frame = cap.read()
    
    if ret == True : 
        cv2.imshow("Frame" ,frame)
        logging.INFO("the camera source is streaming ... ")
        if cv2.waitKey(25) & 0xFF == ord('q') :
            logging.INFO("the camera source stream is stopping ... ")
            break
        
    else :
        break
    
cap.release()
cv2.destroyAllWindows()
   
         




