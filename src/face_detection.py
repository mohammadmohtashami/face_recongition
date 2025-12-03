import cv2 
import matplotlib.pyplot as plt 
import datetime
from config import BASE_DIR , MODEL_PATH , EXIST_MODEL , CLASSES
import os 
import uuid 
from database.insertation import insertation
from ultralytics import YOLO 
import numpy as np 
import openvino as ov 
import ipywidgets as widgets 


if EXIST_MODEL == 0 : 

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
    
else : 
    core = ov.Core()
    device = widgets.Dropdown(
        opetions = core.available_devices + ["AUTO"],
        value = "CPU",
        description = "Device",
        disabled = False
    )
    
    model = core.read_model(model=MODEL_PATH)
    compiled_model = core.compile_model (model=model , 
                    device_name = device.value)
    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    
    height , width = list(input_layer.shape)[1:3]

    classes =  CLASSES
    
    def process_results (frame , results ,thresh):
        h, w = frame.shape [:2]
        
        results = results.squeeze()
        boxes = []
        labels = []
        scores = []
        
        for _ , label , score , xmin ,ymin , xmax , ymax in results:
            
            boxes.append(
                (xmin*w , ymin*h , (xmax - xmin)*w , (ymax - ymin)*h))
                
            
            labels.append(int(label))
            scores.append(float(score))
            
            
            indices = cv2.dnn.NMSBoxes(bboxes=boxes , scores = scores , score_threshold=thresh , nms_threshold=0.6)
            if len(indices) == 0 :
                return []
            
            return [(labels[idx] , scores[idx] , boxes[idx] ) for idx in indices.flatten()]
    
    def draw_boxes (frame , boxes):
        for label , score , box  in boxes : 
            
            x2 = box[0] + box[2]
            y2 = box[1]+ box[3]
            
            cv2.rectangle(img = frame , pt1 = box[:2] , pt2 =(x2 ,y2) , color = (0,255,0) , thickness=3)
            cv2.putText(
                img = frame ,
                text=f"{classes[label]} {score:.2f}",
                org = (box[0] + 10 , box[1]+30),
                fontFace= cv2.FONT_HERSHEY_COMPLEX,
                fontScale=frame.shape[1] /1000 , 
                color=(0 , 255,0),
                thickness=1,
                lineType=cv2.LINE_AA
            )
            
        return frame 
    