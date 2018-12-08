# 作者: 劉冠偉
# 日付: 2017/11/19

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

def write_character_image(img,prefix,name):
    cv2.imwrite("./"+prefix+"/"+prefix + "_" + ("%02d" % name) + "0.jpg", img)


def cutLine(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # ret, img_thres = cv2.threshold(img_gray, 115, 255, cv2.THRESH_BINARY)
    ksize=11
    blur = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    ret,img_thres = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    imgWithLines=img

    height, width = img_thres.shape[:2]
    lines=[]
    lineNum=0

    shadow_width = [0] * width
    print(height, width)

    #计算空白像素的投影的数组
    for x in range(0,width):
        for y in range(0,height):
            if img_thres[y][x] == 0:
                shadow_width[x] = shadow_width[x] + 1
    #绘制空白像素投影
    logFile=open("log.txt","w")
    for x in range(len(shadow_width)):
    #     cv2.line(imgWithLines,(x,0),(x,shadow_width[x]),(0,255,0),1)
        logFile.write("%s," % str(shadow_width[x]))
    
    # TODO: use peak finding
    shadow_width=np.array(shadow_width)
    y1 = signal.savgol_filter(shadow_width, 151, 5)
    indexes1= peakutils.indexes(y1, thres=0.2, min_dist=50)
    lineNum=0
    for index in indexes1:
      lineNum+=1
      endHeight=height-1
      startWidth=index-80
      if startWidth<0: startWidth=0
      endWidth= index+80
      rect = img[0:height, startWidth:endWidth]
      lines.append(rect)
      # cv2.rectangle(imgWithLines, (startWidth,0),(endWidth,endHeight),(0,0,255),2)
      # cv2.putText(imgWithLines, str(lineNum), (startWidth, (endHeight-5)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    print("line num:"+str(len(indexes1)))
    return lines


def getFilename(fullname):
    names=os.path.basename(fullname)
    names=names.split(".")
    return names[0]


if __name__ == "__main__":
    filename = sys.argv[1]
    img = cv2.imread(filename)
    prefixName=getFilename(filename)
    lines = cutLine(img)
    kanji_id = 1
    results=[]
    lineNum=1

    folder=os.path.abspath('./')
    folder=os.path.join(folder,"output",prefixName)

    print(folder)
    if os.path.exists(folder) is False:
        os.mkdir(folder)
    
    for line in reversed(lines):
        # path=("%s%02d\\" %(folder,lineNum))
        path=os.path.join(folder,"%02d"%lineNum)
        print(path)
        if os.path.exists(path) is False:
            os.mkdir(path)
        lineFile=os.path.join(path,"!L%02d.jpg"%lineNum)
        cv2.imwrite(lineFile,line)
        lineNum+=1
        kanjis=detectKanji(line)
        for i in range(len(kanjis)):
            filePath=os.path.join(path,"%02d0.jpg"%i)
            cv2.imwrite(filePath, kanjis[i])