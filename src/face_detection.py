import cv2 
import matplotlib.pyplot as plt 
import datetime
from .config import BASE_DIR , MODEL_PATH , EXIST_MODEL , CLASSES , SAVE_DATA , IMAGE_SAVED_PATH
import os 
import uuid 
from database.insertation import insertation
from ultralytics import YOLO 
import numpy as np 
import openvino as ov 
import ipywidgets as widgets 
from datetime import timedelta
from deepface import DeepFace 

if EXIST_MODEL == 0 : 

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

    image_dir = os.path.join(BASE_DIR , "images")
    os.makedirs(image_dir , exist_ok=True) 

    last_save_time = None
    
    def  detect (img):
        global last_save_time
        
        gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray_img , scaleFactor=1.1 , minNeighbors=5 , minSize=(40 , 40))
        if SAVE_DATA == True:
            for i in range(len(faces)) :
                
                current_time = datetime.datetime.now()
                insertation(f"person{i}",datetime.datetime.now(),uuid.uuid4())

            if last_save_time is None or  (current_time - last_save_time) > timedelta(minutes=1)  :
                now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                image_path = os.path.join(image_dir , now)
                cv2.imwrite(f"{image_path}.jpg" , img)
                last_save_time = datetime.datetime.now()
            
        for (x , y , w ,h ) in faces : 
            cv2.rectangle(img ,(x,y), (x+w , y+h ), (0,255 , 0) , 4)
            cv2.putText(img , text=f"Faces detected : {len(faces)}", org =(20 ,20 ) ,color=(0,255,0) , fontFace=  cv2.FONT_HERSHEY_SIMPLEX , fontScale=0.8
    )
        return img
    
else : 
    desired_persons = IMAGE_SAVED_PATH
    faces_uuid = []
    core = ov.Core()
    device = widgets.Dropdown(
        options = core.available_devices + ["AUTO"],
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
        results_array = results[output_layer]
        results = results_array.squeeze()
        boxes = []
        labels = []
        scores = []
        
        if isinstance(results , dict):
            results = list(results.values())[0]
        
        results = results.T
        
        
        for box in results:
            xcenter , ycenter , w ,h , confidence =box
            xmin = xcenter - w/2
            xmax = xcenter + w/2
            ymin = ycenter - h /2 
            ymax = ycenter + h/2
            
            
            boxes.append(
                (xmin*w , ymin*h , (xmax - xmin)*w , (ymax - ymin)*h))
                
            
            
            scores.append(float(confidence))
            
            
        indices = cv2.dnn.NMSBoxes(bboxes=boxes , scores = [float(s) for s in scores]  , score_threshold=float(thresh) , nms_threshold=0.6)
        if len(indices) == 0 :
                return []
            
        return [(scores[idx] , boxes[idx] ) for idx in indices.flatten()]
    
    def draw_boxes (frame , boxes):
        for  score , box  in boxes : 
            
            x2 = box[0] + box[2]
            y2 = box[1]+ box[3]
            box_int = np.round(box).astype(np.int32)

            
            cv2.rectangle(img = frame , pt1 =box_int[:2] , pt2 =(int(x2) ,int(y2)) , color = (0,255,0) , thickness=3)
            croped_images =crop_image(frame,boxes)
            for image in croped_images : 
                for i in os.listdir(desired_persons):
                    name = i.split(".jpg")[0]
                    backends = ["ssd"]
                    result = DeepFace.verify(img1_path = os.path.join(desired_persons, i), img2_path =image , detector_backends = backends[0])
                    if result['verified'] == True:
                        face_uuid = uuid.uuid4()
                        
                        current_time = datetime.datetime.now()
                        if face_uuid not in faces_uuid and SAVE_DATA == True :
                            insertation(name,current_time ,face_uuid)
                            faces_uuid.append(face_uuid)
                        
                        cv2.putText(
                            img = frame ,
                            text=f"{name} {score:.2f}",
                            org = (box[0] + 10 , box[1]+30),
                            fontFace= cv2.FONT_HERSHEY_COMPLEX,
                            fontScale=frame.shape[1] /1000 , 
                            color=(0 , 255,0),
                            thickness=1,
                            lineType=cv2.LINE_AA
            )           
                    else: 
                        cv2.putText(
                            img = frame ,
                            text=f"{classes[0]} {score:.2f}",
                            org = (box[0] + 10 , box[1]+30),
                            fontFace= cv2.FONT_HERSHEY_COMPLEX,
                            fontScale=frame.shape[1] /1000 , 
                            color=(0 , 255,0),
                            thickness=1,
                            lineType=cv2.LINE_AA
            )           
                    
            
        return frame
    
    def crop_image(img , boxes):
        crops = []
        
        for score ,box in boxes:
            x , y ,w, h = map(int,box)
            
            crops.append(img[ y : y+h  , x:x+w])
        return crops