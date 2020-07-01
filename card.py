import cv2
import numpy as np
import argparse
import imutils
from imutils import  contours

# ap = argparse.ArgumentParser()
# ap.add_argument('-i' , '--image' , required=True)
# ap.add_argument('-r' , '--reference' , required=True)
# agrs = vars(ap.parse_args())

img = cv2.imread('ocr_a_reference.png')
print(img.shape)
cv2.imshow('original',img)
img = cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
img = cv2.threshold(img ,10,255,cv2.THRESH_BINARY_INV)[1]
cv2.imshow('Threshold',img)
cv2.waitKey(0)

refcnts = cv2.findContours(img.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
refcnts = imutils.grab_contours(refcnts)
# print(refcnts)
refcnts = contours.sort_contours(refcnts , method='left-to-right')[0]
# refcnts = sorted(refcnts, key = cv2.contourArea, reverse = True)
# print(refcnts)

FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}

digits = {}

for (i,c) in enumerate(refcnts):
    # print(i)

    # print(c)
    (x,y,w,h) = cv2.boundingRect(c)
    roi = img[y:y+h , x:x+w]
    roi = cv2.resize(roi , (57,88))
    digits[i] = roi
cv2.imshow('ROI',digits[2])
cv2.waitKey(0)

rectkernel = cv2.getStructuringElement(cv2.MORPH_RECT , (9,3))
sqkernel = cv2.getStructuringElement(cv2.MORPH_RECT , (5,5))

print('rectkernel',rectkernel)
img = cv2.imread('credit_card_01.png')
gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
# cv2.imshow('Before' , img)
gray = imutils.resize(gray , width=300)
cv2.imshow('After' , gray)
cv2.waitKey(0)

tophat = cv2.morphologyEx(gray , cv2.MORPH_TOPHAT , rectkernel)
rect = cv2.morphologyEx(gray , cv2.MORPH_RECT , rectkernel)
blackhat = cv2.morphologyEx(gray , cv2.MORPH_BLACKHAT , rectkernel)
close = cv2.morphologyEx(gray , cv2.MORPH_CLOSE , rectkernel)
dilate = cv2.morphologyEx(gray , cv2.MORPH_DILATE , rectkernel)
erode = cv2.morphologyEx(gray , cv2.MORPH_ERODE , rectkernel)
open = cv2.morphologyEx(gray , cv2.MORPH_OPEN , rectkernel)
gradient = cv2.morphologyEx(gray , cv2.MORPH_GRADIENT , rectkernel)
cv2.imshow('Tophat',tophat)
# cv2.imshow('rect',rect)
# cv2.imshow('blackhat',blackhat)
# cv2.imshow('close',close)
# cv2.imshow('dilate',dilate)
# cv2.imshow('erode',erode)
# cv2.imshow('open',open)
# cv2.imshow('gradient',gradient)
cv2.waitKey(0)

gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
gradX = np.absolute(gradX)
(minVal , maxVal) = (np.min(gradX) , np.max(gradX))
# cv2.imshow('BeforegradX',gradX)
gradX = 255*(gradX - minVal)/(maxVal - minVal)
gradX = gradX.astype('uint8')
print('GRADx',gradX)
# cv2.imshow('GRADx' , gradX)
cv2.waitKey(0)

gradX = cv2.morphologyEx(gradX , cv2.MORPH_CLOSE , rectkernel)
# cv2.imshow('Close' , gradX)
thresh = cv2.threshold(gradX , 0 , 255 ,cv2.THRESH_BINARY | cv2.THRESH_OTSU )[1]
# cv2.imshow('thresh' , thresh)
thresh = cv2.morphologyEx(thresh , cv2.MORPH_CLOSE , sqkernel)
cv2.imshow('55',thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts , method='left-to-right')[0]
locs = []
# print(cnts)
for (i,c) in enumerate(cnts):
    (x,y,w,h) = cv2.boundingRect(c)
    ar = w/float(h)
    if ar > 2.5 and  ar < 4.0:

        if (w > 40 and w < 55) and (h > 10 and h < 20):
            locs.append((x, y, w, h))

locs = sorted(locs , key = lambda x:x[0])
output = []

for (i,(gX,gY,gW ,gH)) in enumerate(locs):
    group_output = []
    group = gray[gY-5:gY+gH+5 , gX-5:gX+gW+5]
    cv2.imshow('RR',group)
    group = cv2.threshold(group , 0, 255 , cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    grpcnts = cv2.findContours(group , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    grpcnts = imutils.grab_contours(grpcnts)
    grpcnts = contours.sort_contours(grpcnts , method= 'left-to-right')[0]

    for c in grpcnts:
        (x,y,w,h) = cv2.boundingRect(c)
        roi = group[y:y+h , x:x+w]
        roi = cv2.resize(roi , (57,88))
        cv2.imshow('ROI' , roi)
        scores = []

        for (digit , digitROI) in digits.items():
            result = cv2.matchTemplate(roi , digitROI , cv2.TM_CCOEFF)
            (_,score,_,_) = cv2.minMaxLoc(result)
            scores.append(score)

        group_output.append(str(np.argmax(scores)))

        # cv2.rectangle(img, (gX - 5, gY - 5),(gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
    # cv2.putText(img, "".join(group_output), (gX, gY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        # print(group_output)

        # update the output digits list
        # print(group_output)
    output.extend(group_output)

print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", img)
cv2.waitKey(0)
