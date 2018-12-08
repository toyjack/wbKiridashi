import cv2
import numpy as np
import sys
import peakutils
from scipy import signal

def cutKanji(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # ret, img_thres = cv2.threshold(img_gray, 115, 255, cv2.THRESH_BINARY)
    ksize=11
    blur = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    ret,img_thres = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    imgWithLines=img
    height, width = img_thres.shape[:2]
    lines=[]
    lineNum=0

    shadow_height = [0] * height
    print(height, width)

    #计算空白像素的投影的数组
    for x in range(0,width):
        for y in range(0,height):
            if img_thres[y][x] == 0:
                shadow_height[y] = shadow_height[y] + 1
    #绘制空白像素投影
    logFile=open("log.txt","w")
    for x in range(len(shadow_height)):
        cv2.line(imgWithLines,(0,x),(shadow_height[x],x),(0,255,0),1)
        logFile.write("%s," % str(shadow_height[x]))
    
    # TODO: use peak finding
    shadow_height=np.array(shadow_height)
    # y1 = signal.savgol_filter(shadow_height, 151, 5)
    # indexes1= peakutils.indexes(y1, thres=0.2, min_dist=50)
    # lineNum=0
    # for index in indexes1:
    #   lineNum+=1
    #   endHeight=height-1
    #   startWidth=index-80
    #   if startWidth<0: startWidth=0
    #   endWidth= index+80
    #   rect = img[0:height, startWidth:endWidth]
    #   lines.append(rect)
    #   # cv2.rectangle(imgWithLines, (startWidth,0),(endWidth,endHeight),(0,0,255),2)
    #   # cv2.putText(imgWithLines, str(lineNum), (startWidth, (endHeight-5)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    # print("line num:"+str(len(indexes1)))
    # return lines,imgWithLines
    return [],imgWithLines


def detectKanji(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
    ret3, img_thres = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    height, width = img_thres.shape[:2]
    print("列：", height, width)
    img_shadow = np.zeros((height, width), dtype=np.uint8)
    shadow_height = [0] * height
    global kanji_id
    for x in range(0, (height - 1)):
        for y in range(0, (width - 1)):
            if img_thres[x][y] == 0:
                shadow_height[x] += 1
    # print(shadow_height)
    for i in range(len(shadow_height)):
        for j in range(shadow_height[i]):
            img_shadow[i, j] = 255
    kanji_flag = False
    lie = []
    start = 0
    last = 0
    charNum=0
    for i in range(0, len(shadow_height)):
        if kanji_flag is False and shadow_height[i] >= 5:
            start = i
            kanji_flag = True
        elif kanji_flag is True and (i - start) >= 60 and shadow_height[i] <= 5 and (i - last) >= 50:
            charNum+=1
            kanji_flag = False
            last = i
            startHeight=start-10
            endHeight=i+10
            # cv2.rectangle(img,(0,startHeight),(width,(endHeight-1)),(255,0,0),4)
            # cv2.putText(img, str(charNum), (0,endHeight), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            rect = img[startHeight:endHeight, 0:width]
            print(charNum,startHeight,endHeight, endHeight-startHeight)
            lie.append(rect)
    return lie,img

if __name__ == "__main__":
    filename=sys.argv[1]
    img=cv2.imread(filename)
    lines,imgWithLines=detectKanji(img)
    for x in range(len(lines)):
        cv2.imwrite('./output/'+str(x)+'.jpg',lines[x])
    cv2.namedWindow("shadow",cv2.WINDOW_NORMAL)
    cv2.imshow("shadow",img)
    print("done!")
    cv2.waitKey(0)
    cv2.destroyAllWindows()