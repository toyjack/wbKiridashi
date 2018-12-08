import cv2
import numpy as np
import sys
import os
import peakutils
from scipy import signal

def detectKanji(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
    ret3, img_thres = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    height, width = img_thres.shape[:2]
    print("列：", height, width)
    shadow_height = [0] * height
    global kanji_id
    for x in range(0, (height - 1)):
        for y in range(0, (width - 1)):
            if img_thres[x][y] == 0:
                shadow_height[x] += 1
    # for x in range(len(shadow_height)):
    #     cv2.line(img,(0,x),(shadow_height[x],x),(255,0,0),1)

   
    
    core=cv2.getStructuringElement(cv2.MORPH_RECT,(1,3))
    img_thres=cv2.dilate(img_thres,core,anchor=(0,1),iterations=2)
    img_thres=(255-img_thres)

     # TODO: 輪郭
    image, contours, hierarchy = cv2.findContours(img_thres,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img_thres = cv2.drawContours(img, contours, -1, (0,255,0), 3)

    # for x in range(len(contours)):
    #     area=cv2.contourArea(contours[x])
    #     if area<500 :
    #         continue
    #     if len(contours[x])>0:
    #         rect=contours[x]
            
    #         x,y,w,h=cv2.boundingRect(rect)
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return img_thres



 

if __name__ == "__main__":
    filename=sys.argv[1]
    img=cv2.imread(filename)
    img= detectKanji(img)
    count=1
    # for char in lines:
    #     path=os.path.join('./','test')
    #     if (!os.path.exists(path)):
    #         os.mkdir(path)
    #     cv2.imwrite(os.path.join(path,'%2d0'))

    cv2.namedWindow("window1",cv2.WINDOW_NORMAL)
    cv2.imshow("window1",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()