import cv2
import numpy as np
import copy
import math
import sys
import time
from PIL import Image, ImageDraw, ImageFont
# from appscript import app


# parameters
cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.8  # start point/total width
threshold = 60  # BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0
fontPIL = "arial.ttf"

# variables
isBgCaptured = 0   # bool, whether the background captured
setting = ['e', 'e', 'i', 'c', '2', '0']  # setting optional passcord
input_list = []  # your hand input
auth_flag = 0  # 1 -> success 2-> denied
flick_flag = 0
flick_on = False
place = 0
f = 0
f_time = 0
certain_time = 0
moji = ''


def moji_place(x, y):
    a = (65+(2*x-1)*55//2, 35+(2*y-1)*55//2)
    return a


def flickPalet(place):
    Type = 0
    x = 0
    y = 0
    if place == 0:
        x = 1
        y = 1
        Type = 0
        cv2.putText(img2, '@', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '#', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '/', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '&', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 1:
        x = 2
        y = 1
        Type = 0
        cv2.putText(img2, 'a', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'b', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'c', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '1', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 2:
        x = 3
        y = 1
        Type = 0
        cv2.putText(img2, 'd', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'e', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'f', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '2', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    if place == 3:
        x = 1
        y = 2
        Type = 0
        cv2.putText(img2, 'g', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'h', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'i', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '3', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 4:
        x = 2
        y = 2
        Type = 0
        cv2.putText(img2, 'j', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'k', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'l', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '4', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 5:
        x = 3
        y = 2
        Type = 0
        cv2.putText(img2, 'm', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'n', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'o', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '5', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 6:
        x = 1
        y = 3
        Type = 2
        cv2.putText(img2, 'p', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'q', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'r', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 's', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '6', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 7:
        x = 2
        y = 3
        Type = 1
        cv2.putText(img2, 't', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'u', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'v', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '7', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 8:
        x = 3
        y = 3
        Type = 2
        cv2.putText(img2, 'w', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'x', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'y', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'z', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '8', moji_place(x, y+1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 9:
        x = 1
        y = 4
        Type = 1
        cv2.putText(img2, 'a', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '/', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, 'A', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '9', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 10:
        x = 2
        y = 4
        Type = 1
        cv2.putText(img2, '(', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, ')', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '0', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    elif place == 11:
        x = 3
        y = 4
        Type = 1
        cv2.putText(img2, ',', moji_place(x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '.', moji_place(x-1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '?', moji_place(x, y-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
        cv2.putText(img2, '!', moji_place(x+1, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
    if Type == 0:
        cv2.rectangle(img2, (70+(x-1)*55, 30+y*55), (70+x*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-2)*55, 30+y*55), (70+(x-1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+x*55, 30+y*55), (70+(x+1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-1)*55, 30+(y+1)*55), (70+x*55, 30+y*55),
                      (255, 238, 178), 1)
    if Type == 1:
        cv2.rectangle(img2, (70+(x-1)*55, 30+y*55), (70+x*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-2)*55, 30+y*55), (70+(x-1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+x*55, 30+y*55), (70+(x+1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-1)*55, 30+(y-1)*55), (70+x*55, 30+(y-2)*55),
                      (255, 238, 178), 1)
    if Type == 2:
        cv2.rectangle(img2, (70+(x-1)*55, 30+y*55), (70+x*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-2)*55, 30+y*55), (70+(x-1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+x*55, 30+y*55), (70+(x+1)*55, 30+(y-1)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-1)*55, 30+(y-1)*55), (70+x*55, 30+(y-2)*55),
                      (255, 238, 178), 1)
        cv2.rectangle(img2, (70+(x-1)*55, 30+(y+1)*55), (70+x*55, 30+y*55),
                      (255, 238, 178), 1)


def passcord(setting, input_list, auth_flag):
    if input_list == setting:
        auth_flag = 1
    else:
        input_list.clear()
        auth_flag = 2
    return auth_flag


def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame, learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("apply", fgmask)
    kernel = np.ones((4, 4), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)  # もろふぉじー
    # cv2.imshow("erode", fgmask)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    # cv2.imshow("bitwise", res)
    return res, fgmask


def calculateFingers(res, drawing, img):  # -> finished bool, cnt: finger count
    #  convexity defect
    finger = 0
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing.   (BUG not found)

            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 +
                              (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 +
                              (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) /
                                  (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                    cv2.circle(img, far, 8, [211, 84, 0], -1)

            finger = cnt + 1
            # print(finger)
            return True, cnt, finger
    return False, 0, 0


def checkPlace2(position, certain_time, moji, place):
    if place == 0:
        x, y = 0, 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '@':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '@', certain_time
            else:
                moji = '@'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+x*55 < position[1] < 30+(x+1)*55:
            if moji == '#':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '#', certain_time
            else:
                moji = '#'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == '/':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '/', certain_time
            else:
                moji = '/'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+x*55 < position[1] < 30+(y+1)*55:
            if moji == '&':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '&', certain_time
            else:
                moji = '&'
                certain_time = 0
    if place == 1:
        x, y = 1, 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'a':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'a', certain_time
            else:
                moji = 'a'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'b':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'b', certain_time
            else:
                moji = 'b'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == 'c':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'c', certain_time
            else:
                moji = 'c'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '1':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '1', certain_time
            else:
                moji = '1'
                certain_time = 0
    if place == 2:
        x, y = 2, 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'd':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'd', certain_time
            else:
                moji = 'd'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'e':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'e', certain_time
            else:
                moji = 'e'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == 'f':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'f', certain_time
            else:
                moji = 'f'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '2':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '2', certain_time
            else:
                moji = '2'
                certain_time = 0
    if place == 3:
        x, y = 0, 1
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'g':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'g', certain_time
            else:
                moji = 'g'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'h':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'h', certain_time
            else:
                moji = 'h'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == 'i':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'i', certain_time
            else:
                moji = 'i'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '3':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '3', certain_time
            else:
                moji = '3'
                certain_time = 0
    if place == 4:
        x, y = 1, 1
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'j':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'j', certain_time
            else:
                moji = 'j'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'k':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'k', certain_time
            else:
                moji = 'k'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == 'l':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'l', certain_time
            else:
                moji = 'l'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '4':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '4', certain_time
            else:
                moji = '4'
                certain_time = 0
    if place == 5:
        x, y = 2, 1
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'm':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'm', certain_time
            else:
                moji = 'm'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'n':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'n', certain_time
            else:
                moji = 'n'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == 'o':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'o', certain_time
            else:
                moji = 'o'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '5':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '5', certain_time
            else:
                moji = '5'
                certain_time = 0
    if place == 6:
        x, y = 0, 2
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'p':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'p', certain_time
            else:
                moji = 'p'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'q':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'q', certain_time
            else:
                moji = 'q'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == 'r':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'r', certain_time
            else:
                moji = 'r'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 's':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 's', certain_time
            else:
                moji = 's'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == '6':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '6', certain_time
            else:
                moji = '6'
                certain_time = 0
    if place == 7:
        x, y = 1, 2
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 't':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 't', certain_time
            else:
                moji = 't'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'U':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'u', certain_time
            else:
                moji = 'U'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == 'v':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'v', certain_time
            else:
                moji = 'v'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '7':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '7', certain_time
            else:
                moji = '7'
                certain_time = 0
    if place == 8:
        x, y = 2, 2
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'w':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'w', certain_time
            else:
                moji = 'w'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'x':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'x', certain_time
            else:
                moji = 'x'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == 'y':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'y', certain_time
            else:
                moji = 'y'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'z':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'z', certain_time
            else:
                moji = 'z'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y+1)*55 < position[1] < 30+(y+2)*55:
            if moji == '8':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '8', certain_time
            else:
                moji = '8'
                certain_time = 0
    if place == 9:
        x, y = 0, 3
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == 'a':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'a', certain_time
            else:
                moji = 'a'
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '/':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '/', certain_time
            else:
                moji = '/'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == 'A':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return 'A', certain_time
            else:
                moji = 'A'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '9':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '9', certain_time
            else:
                moji = '9'
                certain_time = 0
    if place == 10:
        x, y = 1, 3
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '(':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '(', certain_time
            else:
                moji = '('
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == ')':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return ')', certain_time
            else:
                moji = ')'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == '0':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '0', certain_time
            else:
                moji = '0'
                certain_time = 0
    if place == 11:
        x, y = 2, 3
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == ',':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return ',', certain_time
            else:
                moji = ','
                certain_time = 0
        if 25+(x)*55 < position[0] < 25+55*(x+1) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '.':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '.', certain_time
            else:
                moji = '.'
                certain_time = 0
        if 25+(x+1)*55 < position[0] < 25+55*(x+2) and 30+(y-1)*55 < position[1] < 30+(y)*55:
            if moji == '?':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '?', certain_time
            else:
                moji = '?'
                certain_time = 0
        if 25+(x+2)*55 < position[0] < 25+55*(x+3) and 30+y*55 < position[1] < 30+(y+1)*55:
            if moji == '!':
                certain_time += 1
                if certain_time > 30:
                    flick_on = False
                    return '!', certain_time
            else:
                moji = '!'
                certain_time = 0
    return moji, certain_time


def checkplace(position, time, place):
    # print(position)
    x, y = 1, 1
    if 70 < position[0] < 125 and 30 < position[1] < 85:
        # print("@#/&")
        if place == 0:
            time += 1
        else:
            place = 0
            time = 0
    elif 125 < position[0] < 180 and 30 < position[1] < 85:
        # print("abc")
        if place == 1:
            time += 1
        else:
            place = 1
            time = 0
    elif 180 < position[0] < 235 and 30 < position[1] < 85:
        # print("def")
        if place == 2:
            time += 1
        else:
            place = 2
            time = 0
    elif 70 < position[0] < 125 and 85 < position[1] < 140:
        # print("ghi")
        if place == 3:
            time += 1
        else:
            place = 3
            time = 0
    elif 125 < position[0] < 180 and 85 < position[1] < 140:
        # print("jkl")
        if place == 4:
            time += 1
        else:
            place = 4
            time = 0
    elif 180 < position[0] < 235 and 85 < position[1] < 140:
        # print("mno")
        if place == 5:
            time += 1
        else:
            place = 5
            time = 0
    elif 70 < position[0] < 125 and 140 < position[1] < 195:
        # print("pqrs")
        if place == 6:
            time += 1
        else:
            place = 6
            time = 0
    elif 125 < position[0] < 180 and 140 < position[1] < 195:
        # print("tuv")
        if place == 7:
            time += 1
        else:
            place = 7
            time = 0
    elif 180 < position[0] < 235 and 140 < position[1] < 195:
        # print("wxyz")
        if place == 8:
            time += 1
        else:
            place = 8
            time = 0
    elif 70 < position[0] < 125 and 195 < position[1] < 250:
        # print("a/A")
        if place == 9:
            time += 1
        else:
            place = 9
            time = 0
    elif 125 < position[0] < 180 and 195 < position[1] < 250:
        # print("()")
        if place == 10:
            time += 1
        else:
            place = 10
            time = 0
    elif 180 < position[0] < 235 and 195 < position[1] < 250:
        # print(",.?!")
        if place == 11:
            time += 1
        else:
            place = 11
            time = 0
    elif 235 < position[0] < 290 and 140 < position[1] < 195:
        # print("delete")
        if place == 12:
            time += 1
            if time > 25:
                place = -1
        else:
            place = 12
            time = 0
    elif 235 < position[0] < 290 and 195 < position[1] < 250:
        # print("enter")
        if place == 13:
            time += 1
            if time > 25:
                place = -2
        else:
            place = 13
            time = 0
    return time, place


camera = cv2.VideoCapture(0)
camera.set(10, 200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)


while camera.isOpened():
    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    # cv2.imshow("smoothing", frame)
    if auth_flag == 0:
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (152, 251, 152), 2)
    if auth_flag == 1:
        cv2.putText(frame, 'Authentication Successfull!!', (0, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (152, 251, 152), 2, cv2.LINE_AA)
    if auth_flag == 2:
        cv2.putText(frame, "Access Denied!!", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 152), 2, cv2.LINE_AA)
        cv2.putText(frame, "Enter 'r' and Retry", (120, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 152), 2, cv2.LINE_AA)
    cv2.imshow('original', frame)
    for i in range(len(input_list)):
        cv2.putText(frame, '{}'.format(input_list[i]), (350+i*27, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (152, 251, 152), 2, cv2.LINE_AA)
    if isBgCaptured == 1:  # this part wont run until background captured
        img, fgmask = removeBG(frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                  int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
        img2 = frame[0:int(cap_region_y_end * frame.shape[0]),
                     int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]
        # cv2.imshow('mask', img)
        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray', gray)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        # cv2.imshow('blur', blur)
        # blur = fgmask[0:int(cap_region_y_end * frame.shape[0]),
        #               int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]
        ret, thresh = cv2.threshold(
            blur, threshold, 255, cv2.THRESH_BINARY)  # 閾値を設定してそれ以上は255黒以下は０白にする
        # ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_OTSU)
        # cv2.imshow('thresh', thresh)

        thresh1 = copy.deepcopy(thresh)
        contours, hierarchy = cv2.findContours(
            thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # coutoursは輪郭の一覧，contourAreaで大きさが見れるhttps://code-graffiti.com/opencv-contour-detection-in-python/
        length = len(contours)
        maxArea = -1
        if length > 0:
            # find the biggest contour (according to area)一番大きい領域について探す，細かい領域は無視して手に注目できるように
            for i in range(length):
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)  # 凸包
            drawing = np.zeros(img.shape, np.uint8)
            top = (500, 500)

            if flick_flag == 0:
                # cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                # cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)
                # for i in range(len(hull)):
                #     a = hull[i][0]
                #     if a[1] < top[1]:
                #         top = a  # 指の先端の座標
                # cv2.drawMarker(drawing, tuple(top), (0, 0, 255),
                #                markerType=cv2.MARKER_STAR, markerSize=10)
                # cv2.imshow('drawing', drawing)
                cv2.drawContours(img2, [res], 0, (0, 255, 0), 2)
                isFinishCal, cnt, finger = calculateFingers(res, drawing, img2)

            if flick_flag == 1:
                alphabet = 0
                for i in range(len(hull)):
                    a = hull[i][0]
                    if a[1] < top[1]:
                        top = a  # 指の先端の座標
                cv2.drawMarker(img2, tuple(top), (0, 0, 255),
                               markerType=cv2.MARKER_STAR, markerSize=10)
                if f_time > 30:
                    flick_on = True
                if f_time < 30:
                    flick_on = False
                if not flick_on:
                    cv2.rectangle(img2, (70+(4-1)*55, 30+4*55), (70+4*55, 30+(4-1)*55),
                                  (255, 238, 178), 1)  # enter
                    cv2.putText(img2, 'enter', (50+(2*4-1)*55//2, 40+(2*4-1)*55//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                    cv2.rectangle(img2, (70+(4-1)*55, 30+3*55), (70+4*55, 30+(3-1)*55),
                                  (255, 238, 178), 1)  # delete
                    cv2.putText(img2, 'delete', (50+(2*4-1)*55//2, 40+(2*3-1)*55//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                    for y in range(4):
                        y += 1
                        for x in range(3):
                            x += 1
                            cv2.rectangle(img2, (70+(x-1)*55, 30+y*55), (70+x*55, 30+(y-1)*55),
                                          (255, 238, 178), 1)
                            if alphabet == 0:
                                cv2.putText(img2, '@#/&', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 1:
                                cv2.putText(img2, 'abc', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 2:
                                cv2.putText(img2, 'def', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 3:
                                cv2.putText(img2, 'ghi', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 4:
                                cv2.putText(img2, 'jkl', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 5:
                                cv2.putText(img2, 'mno', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 6:
                                cv2.putText(img2, 'pqrs', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 7:
                                cv2.putText(img2, 'tuv', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 8:
                                cv2.putText(img2, 'wxyz', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 9:
                                cv2.putText(img2, 'a/A', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 10:
                                cv2.putText(img2, "()", (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            elif alphabet == 11:
                                cv2.putText(img2, ',.?!', (50+(2*x-1)*55//2, 40+(2*y-1)*55//2),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 238, 178), 1, cv2.LINE_AA)
                            alphabet += 1
                    f_time, place = checkplace(top, f_time, place)
                    if place == -1:
                        if input_list == []:
                            input_list.append('*')
                        input_list.pop(-1)
                        print(input_list)
                    if place == -2:
                        auth_flag = passcord(
                            setting, input_list, auth_flag)
                if flick_on:
                    moji, certain_time = checkPlace2(
                        top, certain_time, moji, place)
                    if certain_time > 30:
                        certain_time = 0
                        f_time = 0
                        flick_on = False
                        input_list.append(moji)
                        print(moji)
                        print(input_list)
                    flickPalet(place)

        cv2.imshow('result', img2)

        # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        print("finish")
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(
            0, bgSubThreshold)  # 背景差分法のライブラリ
        isBgCaptured = 1
        flick_on = False
        print('!!!Background Captured!!!')
    # elif k == ord('r'):  # press 'r' to reset the background
    #     bgModel = None
    #     isBgCaptured = 0
    #     print('!!!Reset BackGround!!!')
    elif k == ord('n'):
        print('!!!number mode!!!')
        flick_flag = 0
    elif k == ord('j'):
        print("!!!flick mode!!!")
        flick_flag = 1
        input_list = []
    elif k == ord('r'):
        auth_flag = 0
