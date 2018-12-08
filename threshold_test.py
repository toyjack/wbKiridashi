import cv2 as cv2
import sys

def nothing(x):return x

if __name__ == "__main__":
    filename=sys.argv[1]
    img_origin=cv2.imread(filename)
    thres=127
    ksize=11
    img_gray=cv2.cvtColor(img_origin,cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("control_panel",cv2.WINDOW_NORMAL)
    cv2.namedWindow("thres",cv2.WINDOW_NORMAL)
    cv2.namedWindow("otsu",cv2.WINDOW_NORMAL)
    cv2.createTrackbar("thresbar","control_panel",1,255,nothing)

    while (1):
        thres=cv2.getTrackbarPos("thresbar","control_panel")
        blur = cv2.GaussianBlur(img_gray,(ksize,ksize),0)
        ret, img_thres=cv2.threshold(img_gray,thres,255,cv2.THRESH_BINARY)
        cv2.imshow("thres",img_thres)
        ret3,img_otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow("otsu",img_otsu)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()