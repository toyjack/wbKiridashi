import cv2
import numpy as np
import sys

def cutLine(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # ret, img_thres = cv2.threshold(img_gray, 115, 255, cv2.THRESH_BINARY)
    ksize=11
    blur = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
    ret,img_thres = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    imgWithLines=img

    height, width = img_thres.shape[:2]
    
    lineNum=0

    shadow_width = [0] * width
    print(height, width)

    #计算空白像素的投影的数组
    for x in range(0,width):
        for y in range(0,height):
            if img_thres[y][x] == 0:
                shadow_width[x] = shadow_width[x] + 1
    #绘制空白像素投影
    # logFile=open("log.txt","w")
    # for x in range(len(shadow_width)):
    #     cv2.line(imgWithLines,(x,0),(x,shadow_width[x]),(255,0,0),1)
    #     logFile.write("%s\n" % str(shadow_width[x]))



    flag = False
    lines = []
    start = 0
    last= 0
    for i in range(0, len(shadow_width)):
        if flag is False and shadow_width[i] >= 300:
            start = i
            flag = True
        elif flag is True and (i - start) > 20 and shadow_width[i] < 300 and (i-last)>80:
            flag = False
            # startWidth=start-10
            # endWidth= i+20
            last=i
            lineNum+=1
            startWidth=start-30
            if startWidth<0: startWidth=0
            endWidth= i+30
            print(str(startWidth)+",0 " +str(endWidth)+","+str(height)+":"+str(shadow_width[i]))
            # cv2.rectangle(imgWithLines, (startWidth,0),(endWidth,height),(0,0,255),2)
            # cv2.putText(imgWithLines, str(lineNum), (startWidth, height), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            rect = img[0:height, startWidth:endWidth]
            lines.append(rect)
            print("行の検出が完了しました")
    print(lineNum)
    return lines,imgWithLines

if __name__ == "__main__":
    filename=sys.argv[1]
    img=cv2.imread(filename)
    # img = cv2.imread('./1.jpg')
    lines, imgWithLines = cutLine(img)
    # for i in range(len(lines)):
    #     cv2.imwrite("./test/"+ ("%02d" % i) + ".jpg", lines[i])
    cv2.namedWindow("shadow",cv2.WINDOW_NORMAL)
    cv2.imshow("shadow",imgWithLines)
    print("done!")
    cv2.waitKey(0)
    cv2.destroyAllWindows()