import json
import time
import datetime
import requests
MIDPOINT_X = 0.8288235664367676
MIDPOINT_Y =  0.77963986992836
URL="https://lbhack.herokuapp.com"
WIDTH=640
HEIGHT=480


SLACK_X =0.1
SLACK_Y = 0.1

import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def getActivity(x,y):
    if x <= WIDTH/2 - 100  and y <=HEIGHT/2 - 100:
        return 0
    elif x > WIDTH/2 + 100 and y <=HEIGHT/2 - 100:
        return 1
    elif x <= WIDTH/2  - 100 and y>HEIGHT/2 + 100 :
        return 2
    elif x >= WIDTH/2 + 100 and y > HEIGHT/2 + 100:
        return 3
    return 4


import argparse
import math
def localize_objects(path,tmp,hr_tmp,idnty):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations
    
    #print(objects)
    json_ans=dict()    
    ts=time.time()
    hr=datetime.datetime.fromtimestamp(ts).strftime('%H')
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    if hr!=hr_tmp:
        idnty = 0
        tmp["activity0Counter"]=0
        tmp["activity1Counter"]=0
        tmp["activity2Counter"]=0
        tmp["activity3Counter"]=0
    
    for obj in objects:
        if 'fish' in obj.name.lower() or obj.name.lower() == "animal":            
            json_ans.update({'timestamp':st})
            json_ans.update({'date':datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')})
            json_ans.update({'time':datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')})
            #json_ans.update({"id":tmp["id"]+1})
            idnty = idnty + 1                    
            vertices=obj.bounding_poly.normalized_vertices
            x_avg,y_avg=0,0
            for coordinate in vertices:
                x_avg=x_avg + coordinate.x
                y_avg= y_avg + coordinate.y
            x_avg = x_avg/4.0
            y_avg = y_avg/4.0
            
            json_ans.update({"midX":x_avg})
            json_ans.update({"midY":y_avg})
                      

            distance = round(math.sqrt((x_avg-tmp["midX"])**2+(y_avg-tmp["midY"])**2),2)
            json_ans.update({'distance':distance})

            if distance==0:
                json_ans.update({"awake":0})
                json_ans.update({"rate":0})
            else:
                json_ans.update({"awake":1})
                json_ans.update({"rate":distance/2})

                
            activity=getActivity(x_avg*WIDTH,y_avg*HEIGHT)
            print(activity)
            json_ans.update({"activity":activity})

                
            json_ans.update({"activity1Counter":tmp["activity1Counter"]})
            json_ans.update({"activity2Counter":tmp["activity2Counter"]})
            json_ans.update({"activity3Counter":tmp["activity3Counter"]})
            json_ans.update({"activity0Counter":tmp["activity0Counter"]})\

            
            currentURL = URL + "/current"
            if activity==1:
                json_ans.update({"activity1Counter":tmp["activity1Counter"]+1})
                requests.post(url = currentURL, data={"activity": "drink"}) 
            elif activity==2:
                json_ans.update({"activity2Counter":tmp["activity2Counter"]+1})
                requests.post(url = currentURL, data={"activity": "sleep" }) 
            elif activity==3:
                json_ans.update({"activity3Counter":tmp["activity3Counter"]+1})
                requests.post(url = currentURL, data={"activity": "eat"}) 
            elif activity == 0:
                json_ans.update({"activity0Counter":tmp["activity0Counter"]+1})
                requests.post(url = currentURL, data={"activity": "play" }) 
            return json_ans,hr,idnty, True

    return json_ans, hr, idnty, False

import cv2
import numpy as np

hr=0
idnty=0
PARAMS={"id":0,"activity":0,"activity1Counter":0,"activity2Counter":0,"activity3Counter":0,"activity0Counter":0,"timestamp":"","date":" ","time":" ","distance":0,"awake":-1,"midX":0,"midY":0,"rate":0}
        
cap = cv2.VideoCapture(0)
print(cap.get(3))
print(cap.get(4))
w, h = (26, 26)
while True:
    ret, frame = cap.read()
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


    cv2.imwrite("fish.jpg", frame)
    a, b, c, flag = localize_objects("fish.jpg", PARAMS, hr, idnty)
    if (flag):
        PARAMS = a
        hr = b
        idnty = c
        cv2.imwrite("fish2.jpg", frame)
        #r = requests.post(url = URL, data=PARAMS)
    cv2.imshow("video", frame) 



    
    # elif key == ord('s'):
    #     PARAMS, hr, idnty, flag = localize_objects("fish.jpg", PARAMS, hr, idnty)
        
    #     #if idnty2==idnty:
    #     if (flag):
    #         cv2.putText(frame, "Fish", (round(PARAMS["midX"]*cap.get(3)), round(PARAMS["midY"]*cap.get(4))),
    #         cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    #         print((round(PARAMS["midX"]*100), round(PARAMS["midY"]*100)))
    #         cv2.imwrite("fish2.jpg", frame)
    
     
    # cv2.imwrite("fish.jpg", frame)
    # PARAMS, hr, idnty, flag = localize_objects("fish.jpg", PARAMS, hr, idnty)
        
    #     #if idnty2==idnty:
    # if (flag):
    #     cv2.putText(frame, "Fish", (round(PARAMS["midX"]*cap.get(3)), round(PARAMS["midY"]*cap.get(4))),
    #     cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    #     cv2.imwrite("fish2.jpg", frame)
    # cv2.imshow("video", frame) 

    #r = requests.post(url = URL, data=PARAMS) 


cap.release()
cv2.destroyAllWindows()
       
#PARAMS,hr,idnty=localize_objects("/Users/indumanimaran/Documents/Hackathon/BeachHacks/fish2.jpg",PARAMS,hr,idnty)
#r = requests.post(url = URL, data=PARAMS) 

