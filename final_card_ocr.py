import cv2
import imutils
from imutils import contours
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help = "Path to input image")
args = vars(ap.parse_args())

image_path = args['image']
font_path_d = 'font_images/OCRA.png'
font_path_a = 'font_images/ocr_a_reference.png'



# Finding contours of the initial digits/alphabets(FONT) and then storing their ROI's in a dictionary
def find_ROI(path):
    img = cv2.imread(path)
    # cv2.imshow('original', img)
    # cv2.waitKey(0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('thresholded', thresh)
    # cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts, method='left-to-right')[0]


    sample = {}
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        roi = thresh[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))
        sample[i] = roi

    return sample


# Preprocessing original image and finding its contours
def preprocessing_find_contours(path):

    rectkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    sqkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Before' , img)
    gray = imutils.resize(gray, width=300)
    # print(gray.shape)
    # cv2.imshow('After', gray)
    # cv2.waitKey(0)

    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectkernel)
    # cv2.imshow('Tophat', tophat)
    # cv2.waitKey(0)

    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    # cv2.imshow('BeforegradX',gradX)

    gradX = 255 * (gradX - minVal) / (maxVal - minVal)
    gradX = gradX.astype('uint8')
    # print('GRADx', gradX)
    # cv2.imshow('GRADx' , gradX)
    # cv2.waitKey(0)

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectkernel)
    # cv2.imshow('Close' , gradX)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imshow('thresh' , thresh)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqkernel)
    # cv2.imshow('55', thresh)
    # cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts, method='left-to-right')[0]

    return cnts



sample = find_ROI(font_path_d)
digits = find_ROI(font_path_a)
# cv2.imshow('sds',digits[0])
# cv2.imshow('da',sample[10])
# cv2.waitKey(0)

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

FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}



cnts = preprocessing_find_contours(image_path)



def for_digits(cnts,path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = imutils.resize(gray, width=300)

    locs_d = []
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if ar > 2.5 and ar < 4.0:

            if (w > 40 and w < 55) and (h > 10 and h < 20):
                locs_d.append((x, y, w, h))

    locs_d = sorted(locs_d, key=lambda x: x[0])

    output = []

    for (i, (gX, gY, gW, gH)) in enumerate(locs_d):
        group_output = []
        group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
        # cv2.imshow('RR', group)
        group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        grpcnts = cv2.findContours(group, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        grpcnts = imutils.grab_contours(grpcnts)
        grpcnts = contours.sort_contours(grpcnts, method='left-to-right')[0]

        for c in grpcnts:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = group[y:y + h, x:x + w]
            roi = cv2.resize(roi, (57, 88))
            # cv2.imshow('ROI', roi)
            scores = []

            for (digit, digitROI) in digits.items():
                result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
                (_, score, _, _) = cv2.minMaxLoc(result)
                scores.append(score)

            group_output.append(str(np.argmax(scores)))

            # cv2.rectangle(img, (gX - 5, gY - 5),(gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
        # cv2.putText(img, "".join(group_output), (gX, gY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        # print(group_output)

        # update the output digits list
        # print(group_output)
        output.extend(group_output)
    return output


def for_alphabets(cnts,path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = imutils.resize(gray, width=300)

    locs_a = []
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        if y > 145 and y < (gray.shape[0] - 8) and x < (gray.shape[1] * 5 / 8) and x > 10:
            locs_a.append((x, y, w, h))

    locs_a = sorted(locs_a, key=lambda x: x[0])

    output = ''

    for (i, (gX, gY, gW, gH)) in enumerate(locs_a):
        group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
        # cv2.imwrite(' z{}.jpg'.format(i), group)
        group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.waitKey(0)

        grpcnts = cv2.findContours(group, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        grpcnts = imutils.grab_contours(grpcnts)
        grpcnts = contours.sort_contours(grpcnts, method='left-to-right')[0]

        card_name = ''
        for c in grpcnts:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = group[y:y + h, x:x + w]
            roi = cv2.resize(roi, (57, 88))
            scores = []

            for i in range(len(char)):
                result = cv2.matchTemplate(roi, char[i][1], cv2.TM_CCOEFF)
                (_, score, _, _) = cv2.minMaxLoc(result)
                scores.append(score)

            # print('Scores',len(scores))
            index_max_score = np.argmax(scores)
            # print(index_max_score)
            card_name = card_name + char[index_max_score][0]
        # print(card_name)
        output = output + " " + card_name

    # print(output)
    return output

output_d = for_digits(cnts , image_path)
output_a = for_alphabets(cnts , image_path)


print('RESULT...................')
print()
print("Card Number           : {}".format("".join(output_d)))
print()
print("Card Type:            : {}".format(FIRST_NUMBER[output_d[0]]))
print()
print('Card Holder Name      : {}'.format(output_a))