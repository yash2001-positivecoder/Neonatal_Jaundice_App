from flask import Flask, render_template, request, redirect
import base64
from pickle import TRUE
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import *
import seaborn as sns
import mediapipe as mp
import pickle
from scipy import spatial
import skimage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    data_url = data['value']
    _, data = data_url.split(",", 1)
    image_data = base64.b64decode(data)
    np_array = np.frombuffer(image_data, dtype=np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    listx=[]
    listy=[]
    listxy=[]

    values={}
    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
    drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
    

    # img = cap
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("43")
    results = faceMesh.process(imgRGB)
    print("45")
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,
            #                         drawSpec,drawSpec)

            for id,lm in enumerate(faceLms.landmark):
                # print(lm)
                # print(id)
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                # print(id,x,y)
                
                list_temp=[]
                list_temp.append(x)
                list_temp.append(y)
                listxy.append(list_temp)
                values[id]=list_temp
                del list_temp
        l=np.array(listxy) 
        # print(values)
        leye=[]
        reye=[]
        lips=[]
        rbrow=[]
        lbrow=[]
        lefteye=[466, 388, 387, 386, 385, 384, 398,263, 249, 390, 373, 374, 380, 381, 382, 362,467, 260, 259, 257, 258, 286, 414,359, 255, 339, 254, 253, 252, 256, 341, 463,342, 445, 444, 443, 442, 441, 413,446, 261, 448, 449, 450, 451, 452, 453, 464,372, 340, 346, 347, 348, 349, 350, 357, 465]
        nose=[168,1,2,98,327,205,425]
        righteye=[246, 161, 160, 159, 158, 157, 173,33, 7, 163, 144, 145, 153, 154, 155, 133,247, 30, 29, 27, 28, 56, 190,130, 25, 110, 24, 23, 22, 26, 112, 243,113, 225, 224, 223, 222, 221, 189,226, 31, 228, 229, 230, 231, 232, 233, 244,143, 111, 117, 118, 119, 120, 121, 128, 245]
        mouth=[61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291,146, 91, 181, 84, 17, 314, 405, 321, 375, 291,78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308,78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
        rightbrow=[156, 70, 63, 105, 66, 107, 55, 193,35, 124, 46, 53, 52, 65]
        leftbrow=[383, 300, 293, 334, 296, 336, 285, 417,265, 353, 276, 283, 282, 295]


    
        for i in lefteye:
            leye.append(values[i])
        for i in righteye:
            reye.append(values[i])
        for i in mouth:
            lips.append(values[i])        
        for i in rightbrow:
            rbrow.append(values[i]) 
        for i in leftbrow:
            lbrow.append(values[i])     
        eyer=np.array(reye)
        eyel=np.array(leye)
        lip=np.array(lips)
        browr=np.array(rbrow)
        browl=np.array(lbrow)
        vertice = spatial.ConvexHull(l).vertices
        Y1, X1 = skimage.draw.polygon(l[vertice, 1], l[vertice, 0])
        cropped_img = np.zeros(img.shape, dtype=np.uint8)
        cropped_img[Y1, X1] = img[Y1, X1]
                
        left_eye = spatial.ConvexHull(eyel).vertices
        Y2, X2 = skimage.draw.polygon(eyel[left_eye, 1], eyel[left_eye, 0])
        right_eye = spatial.ConvexHull(eyer).vertices
        Y3, X3 = skimage.draw.polygon(eyer[right_eye, 1], eyer[right_eye, 0])
        mouth_lip = spatial.ConvexHull(lip).vertices
        Y4, X4 = skimage.draw.polygon(lip[mouth_lip, 1], lip[mouth_lip, 0])
        right_brow = spatial.ConvexHull(browr).vertices
        Y5, X5 = skimage.draw.polygon(browr[right_brow, 1], browr[right_brow, 0])
        left_brow = spatial.ConvexHull(browl).vertices
        Y6, X6 = skimage.draw.polygon(browl[left_brow, 1], browl[left_brow, 0])


        simple=cropped_img
        simple[Y2,X2]=0
        simple[Y3,X3]=0
        simple[Y4,X4]=0
        simple[Y5,X5]=0
        simple[Y6,X6]=0

        rsum=0
        bsum=0
        gsum=0
        black=0
        blist=[]
        rlist=[]
        glist=[]
        x,y,z=cropped_img.shape
        rsum=0
        bsum=0
        gsum=0
        black=0
        for i in cropped_img:  
            for j in i:
                if((j[0]==0 and j[1]==0 and j[2]==0) or (j[0]==0 and j[1]==0) or (j[1]==0 and j[2]==0) or (j[0]==0 and j[2]==0) or j[0]==0 or j[1]==0 or j[2]==0 or (j[0] <60) or (j[1] <60) or (j[2] <60)):
                    black=black+1
                else:    
                    bsum=bsum+j[0]
                    blist.append(j[0])
                    gsum=gsum+j[1]
                    glist.append(j[1])
                    rsum=rsum+j[2]
                    rlist.append(j[2])

        bavg=ceil(bsum/(x*y-black))
        ravg=ceil(rsum/(x*y-black))
        gavg=ceil(gsum/(x*y-black))
        blist=[bavg]
        rlist=[ravg]
        glist=[gavg]
        one=[ravg,gavg,bavg]
        print(one)
        t=np.array(one)
        t.shape=(1,3)

        model=pickle.load(open("model2.pkl","rb"))
        val=model.predict(t)
        v=val[0]
        dict = {'value' : v}
    return dict

if __name__ == '__main__':
    app.run(debug=True)