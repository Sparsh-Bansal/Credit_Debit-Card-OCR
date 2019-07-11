import cv2
import imutils
from imutils import contours
import numpy as np

img = cv2.imread('OCRA.png')
cv2.imshow('original',img)
gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray , 10 , 255 , cv2.THRESH_BINARY_INV)[1]
cv2.imshow('thresholded',thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts , method='left-to-right')[0]

sample = {}
for (i,c) in enumerate(cnts):
    (x,y,w,h) = cv2.boundingRect(c)
    roi = thresh[y:y+h , x:x+w]
    roi = cv2.resize(roi , (57,88))
    sample[i] = roi

# for i in range(len(sample)):
    # cv2.imwrite('{}.jpg'.format(i),sample[i])

char = {
    0 : ['A' , sample[1]],
    1 : ['B', sample[7]],
    2 : ['C', sample[12]],
    3 : ['D', sample[17]],
    4 : ['E', sample[22]],
    5 : ['F', sample[27]],
    6 : ['G', sample[32]],
    7 : ['H', sample[36]],
    8 : ['I', sample[42]],
    9 : ['J', sample[50]],
    10 : ['K', sample[54]],
    11 : ['L', sample[60]],
    12 : ['M', sample[67]],
    13 : ['N', sample[73]],
    14 : ['O', sample[82]],
    15 : ['P', sample[87]],
    16 : ['Q', sample[0]],
    17 : ['R', sample[6]],
    18 : ['S', sample[11]],
    19 : ['T', sample[16]],
    20 : ['U', sample[21]],
    21 : ['V', sample[26]],
    22 : ['W', sample[31]],
    23 : ['X', sample[35]],
    24 : ['Y', sample[41]],
    25 : ['Z', sample[47]],
    26 : ['A', sample[3]],
    27 : ['B', sample[9]],
    28 : ['C', sample[14]],
    29 : ['D', sample[19]],
    30 : ['E', sample[24]],
    31 : ['F', sample[29]],
    32 : ['G', sample[34]],
    33 : ['H', sample[38]],
    34 : ['I', sample[44]],
    35 : ['J', sample[49]],
    36 : ['K', sample[56]],
    37 : ['L', sample[62]],
    38 : ['M', sample[68]],
    39 : ['N', sample[74]],
    40 : ['O', sample[83]],
    41 : ['P', sample[88]],
    42 : ['Q', sample[2]],
    43 : ['R', sample[8]],
    44 : ['S', sample[13]],
    45 : ['T', sample[18]],
    46 : ['U', sample[23]],
    47 : ['V', sample[28]],
    48 : ['W', sample[33]],
    49 : ['X', sample[37]],
    50 : ['Y', sample[43]],
    51 : ['Z', sample[48]],
}
cv2.imshow('Sample',char[51][1])
rectkernel = cv2.getStructuringElement(cv2.MORPH_RECT , (9,3))
sqkernel = cv2.getStructuringElement(cv2.MORPH_RECT , (5,5))

img = cv2.imread('credit_card_04.png')
gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
# cv2.imshow('Before' , img)
gray = imutils.resize(gray , width=300)
print(gray.shape)
cv2.imshow('After' , gray)
cv2.waitKey(0)

tophat = cv2.morphologyEx(gray , cv2.MORPH_TOPHAT , rectkernel)
cv2.imshow('Tophat',tophat)
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
sample = {}
for (i,c) in enumerate(cnts):
    (x,y,w,h) = cv2.boundingRect(c)
    # print(i)
    # print(x,y,w,h)
    # roi = tophat[y:y+h , x:x+w]
    # roi = cv2.resize(roi , (100,100))
    # cv2.imwrite('z{}.jpg'.format(i),roi)
    if y>145 and y < (gray.shape[0]-8) and x < (gray.shape[1]*5/8) and x>10:
        locs.append((x,y,w,h))
print(locs)

locs = sorted(locs , key= lambda x:x[0])
output = ''

for (i,(gX,gY,gW,gH)) in enumerate(locs):
    group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
    cv2.imwrite(' z{}.jpg'.format(i) , group)
    group = cv2.threshold(group , 0 , 255 , cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.waitKey(0)

    grpcnts = cv2.findContours(group , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    grpcnts = imutils.grab_contours(grpcnts)
    grpcnts = contours.sort_contours(grpcnts , method= 'left-to-right')[0]

    card_name = ''
    for c in grpcnts:
        (x,y,w,h) = cv2.boundingRect(c)
        roi = group[y:y+h , x:x+w]
        roi = cv2.resize(roi , (57,88))
        scores = []

        for i in range(len(char)):
            result = cv2.matchTemplate(roi , char[i][1] , cv2.TM_CCOEFF)
            (_,score,_,_) = cv2.minMaxLoc(result)
            scores.append(score)

        # print('Scores',len(scores))
        index_max_score = np.argmax(scores)
        # print(index_max_score)
        card_name = card_name + char[index_max_score][0]
    print(card_name)
    output = output + " " + card_name

print(output)