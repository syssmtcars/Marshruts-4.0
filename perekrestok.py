import cv2  # библиотека opencv
import numpy  # работа с массивамиpip3 install paho-mqtt
import paho.mqtt.client as mqtt
import math



cap = cv2.VideoCapture(2)  # читать видео поток
cap.set(cv2.CAP_PROP_BRIGHTNESS,1)
handle = open("red.txt", "r")
h_down_g = int(handle.readline())
s_down_g = int(handle.readline())
v_down_g = int(handle.readline())
h_up_g = int(handle.readline())
s_up_g = int(handle.readline())
v_up_g = int(handle.readline())

handle2 = open('cropMe.txt','r')
handle3 = open(str(input()+'.txt'),'w')


x=int(handle2.readline())
y=int(handle2.readline())
h=int(handle2.readline())
w=int(handle2.readline())

while True:
    _, image_original = cap.read()
    image = image_original[y:y + h, x:x + w]
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    #cv2.rectangle(image, (300,20),(20,20),  (255, 0, 255))  # рисуем прямоугольник
    mask = cv2.inRange(img_hsv, numpy.array([h_down_g, s_down_g, v_down_g]), numpy.array([h_up_g, s_up_g, v_up_g]))
    _, contours0, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # перебираем все найденные контуры в цикле

    for cnt in contours0:
         rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
         box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
         box = numpy.int0(box)  # округление координат
         area = int(rect[1][0] * rect[1][1])  # вычисление площади
         center = (int(rect[0][0]), int(rect[0][1]))
         print(center)
         if area > 100:
             k = center
             #print(str(center))
             #client.publish("center", str(center))
             #cv2.drawContours(image, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник
             cv2.rectangle(image,(center[0]-50,center[1]-50),(center[0]+50,center[1]+50),(255,0,0))
    cv2.imshow("mask", mask)
    cv2.imshow("original", image)
    cv2.imshow("HSV", img_hsv)
    if cv2.waitKey(1) == 27:
        # client.disconnect()
        break



c10 = k[0]-50
c11 = k[1]-50

c20 = k[0]+50
c21 = k[1]+50

#(center[0]+50,center[1]+50)

#print(box)
handle3.write(str(c10) + '\n')
handle3.write(str(c11) + '\n')
handle3.write(str(c20) + '\n')
handle3.write(str(c21) + '\n')



handle3.close()
