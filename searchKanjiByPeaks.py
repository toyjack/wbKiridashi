import cv2
import numpy as np
import sys
import os
import peakutils
from scipy import signal

def detectKanji(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
    ret3, img_thres = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    height, width = img_thres.shape[:2]
    print("列：", height, width)
    shadow_height = [0] * height
    global kanji_id
    for x in range(0, (height - 1)):
        for y in range(0, (width - 1)):
            if img_thres[x][y] == 0:
                shadow_height[x] += 1
    
    shadow_height=np.array(shadow_height)
    y1 = signal.savgol_filter(shadow_height, 151, 5)
    # for x in range (len(y1)):
    #     cv2.line(img,(0,x),(int(y1[x]),x),(0,255,0),1)
    indexes1= peakutils.indexes(y1, thres=0.1, min_dist=80)
    lineNum=0
    lines=[]
    for index in indexes1:
      lineNum+=1
    #   cv2.putText(img, str(lineNum), (int(y1[index]),index), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
      startHeight=index-75
      if startHeight<0:startHeight=0
      endHeight=index+75
      rect = img[startHeight:endHeight, 0:width]
      lines.append(rect)

    print("line num:"+str(len(indexes1)))
    return lines

if __name__ == "__main__":
    filename=sys.argv[1]
    img=cv2.imread(filename)
    lines= detectKanji(img)
    count=1
    for char in lines:
        path=os.path.join('./','test')
        if os.path.exists(path) is False:
            os.mkdir(path)
        cv2.imwrite(os.path.join(path,'%2d0.jpg'%count),char)
        count+=1

    cv2.namedWindow("window1",cv2.WINDOW_NORMAL)
    cv2.imshow("window1",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()