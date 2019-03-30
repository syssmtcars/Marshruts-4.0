import cv2  # библиотека opencv
import numpy  # работа с массивамиpip3 install paho-mqtt
import paho.mqtt.client as mqtt
import math

handle2 = open(str(input())+'.txt','w')

cap = cv2.VideoCapture(2)  # читать видео поток

handle = open("red.txt", "r")
h_down_g = int(handle.readline())
s_down_g = int(handle.readline())
v_down_g = int(handle.readline())
h_up_g = int(handle.readline())
s_up_g = int(handle.readline())
v_up_g = int(handle.readline())
#print(h_up, h_down, s_up, s_down, v_up, v_down)
# h_up_g = 139#115
# s_up_g = 84#255
# v_up_g = 185#255
# h_down_g = 0#81
# s_down_g = 0#155
# v_down_g = 0#70
center=0
center1=0
center2=0
while True:
    _, image = cap.read()
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    img_hsv = cv2.GaussianBlur(img_hsv, (5, 5), 2)
    mask = cv2.inRange(img_hsv, numpy.array([h_down_g, s_down_g, v_down_g]), numpy.array([h_up_g, s_up_g, v_up_g]))
    _, contours0, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # перебираем все найденные контуры в цикле
    for cnt in contours0:
        rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = numpy.int0(box)  # округление координат
        area = int(rect[1][0] * rect[1][1])  # вычисление площади

        if area > 10:
            center = (int(rect[0][0]), int(rect[0][1]))
            if center[0]>300:
                center1=center
            else:
                center2=center
            print("center 1 =", center1)
            print("center 2 =", center2)
            x1 = box[0][0]
            y1 = box[0][1]
            x2 = box[1][0]
            y2 = box[1][1]
            x3 = box[2][0]
            y3 = box[2][1]
            x4 = box[3][0]
            y4 = box[3][1]
            cv2.drawContours(image, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник
            cv2.circle(image, center, 1, (0, 255, 0), 2)
    cv2.imshow("mask", mask)
    cv2.imshow("original", image)
    cv2.imshow("HSV", img_hsv)
    if cv2.waitKey(1) == 27:
        # client.disconnect()
        break


x=center2[0]
y=center2[1]
h=center1[1]-center2[1]
w=center1[0]-center2[0]

handle2.write(str(x) + '\n')
handle2.write(str(y) + '\n')
handle2.write(str(h) + '\n')
handle2.write(str(w) + '\n')
handle2.close()