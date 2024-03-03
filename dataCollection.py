import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 400

folder = "Data/A"
counter = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # create a numpy array forwhite image
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        
        # adding pixel (offset) to get bigger image
        # 
        imgCrop = img[y - offset:y+ h+offset, x - offset:x + w+offset]
        
        


        
        aspectRatio = h/w
        if aspectRatio > 1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            
            # 
            imgResizeSahpe = imgResize.shape
            
            wGap = math.ceil((imgSize-wCal)/2)
            # copy the `img` on imgWhite
            imgWhite[:, wGap:wCal+wGap] = imgResize
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            
            # 
            imgResizeSahpe = imgResize.shape
            
            hGap = math.ceil((imgSize-hCal)/2)
            # copy the `img` on imgWhite
            imgWhite[hGap:hCal+hGap, :] = imgResize            
            
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImgWhite", imgWhite)
        
        
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    if key == ord("s"):
        counter+=1
        cv2.imwrite(f"{folder}/Image_{time.time()}.jpg", imgWhite)
        print(counter)
    elif key == 17:
        # 
        # break on ctrl+q
        break
    else:
        print(key)
    
    
cap.release()
cv2.destroyAllWindows()