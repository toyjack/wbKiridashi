import cv2
import numpy as np
import sys
# TODO:use peak-finding
import peakutils
from scipy import signal

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
    return lines,imgWithLines

if __name__ == "__main__":
    filename=sys.argv[1]
    img=cv2.imread(filename)
    lines, imgWithLines = cutLine(img)
    for i in range(len(lines)):
        cv2.imwrite("./test/"+ ("%02d" % i) + ".jpg", lines[i])
    # cv2.namedWindow("shadow",cv2.WINDOW_NORMAL)
    # cv2.imshow("shadow",imgWithLines)
    print("done!")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()