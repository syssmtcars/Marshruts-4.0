import cv2
import numpy
import paho.mqtt.client as mqtt

cap = cv2.VideoCapture(2)



handle = open("red.txt", "r")
h_down_g = int(handle.readline())
s_down_g = int(handle.readline())
v_down_g = int(handle.readline())
h_up_g = int(handle.readline())
s_up_g = int(handle.readline())
v_up_g = int(handle.readline())

handle2 = open('cropMe.txt', 'r')
handle3 = open('a1.txt', 'r')
handle4 = open('a2.txt', 'r')
handle5 = open('a3.txt','r')
handle6 = open('b1.txt','r')
handle7 = open('b2.txt','r')
handle8 = open('b3.txt','r')
handle9 = open('yellow.txt','r')

x = int(handle2.readline())
y = int(handle2.readline())
h = int(handle2.readline())
w = int(handle2.readline())

a11 = int(handle3.readline())
a12 = int(handle3.readline())
a13 = int(handle3.readline())
a14 = int(handle3.readline())

a21 = int(handle4.readline())
a22 = int(handle4.readline())
a23 = int(handle4.readline())
a24 = int(handle4.readline())

a31 = int(handle5.readline())
a32 = int(handle5.readline())
a33 = int(handle5.readline())
a34 = int(handle5.readline())

b11 = int(handle6.readline())
b12 = int(handle6.readline())
b13 = int(handle6.readline())
b14 = int(handle6.readline())

b21 = int(handle7.readline())
b22 = int(handle7.readline())
b23 = int(handle7.readline())
b24 = int(handle7.readline())

b31 = int(handle8.readline())
b32 = int(handle8.readline())
b33 = int(handle8.readline())
b34 = int(handle8.readline())

h_down = int(handle9.readline())
s_down = int(handle9.readline())
v_down = int(handle9.readline())

h_up = int(handle9.readline())
s_up = int(handle9.readline())
v_up = int(handle9.readline())

red_inzone = (51,0,255)

client = mqtt.Client()
client.connect('192.168.1.141')

while True:
    _, image_original = cap.read()
    image = image_original[y:y + h, x:x + w]

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

    mask = cv2.inRange(img_hsv, numpy.array([h_down, s_down, v_down]), numpy.array([h_up, s_up, v_up]))
    _, contours0, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    center_a1 = (int((a13 - a11) / 2) + a11, int((a24 - a12) / 2) + a12)
    center_a2 = (int((a23 - a21) / 2) + a21, int((a24 - a22) / 2) + a22)
    center_a3 = (int((a33-a31)/2)+a31,int((a34-a32)/2)+a32)
    center_b1 = (int((b13 - b11) / 2) + b11, int((b14 - b12) / 2) + b12)
    center_b2 = (int((b23 - b21) / 2) + b21, int((b24 - b22) / 2) + b22)
    center_b3 =(int((b33-b31)/2)+b31,int((b34-b32)/2)+b32)


    for cnt in contours0:
         rect = cv2.minAreaRect(cnt)
         box = cv2.boxPoints(rect)
         box = numpy.int0(box)
         area = int(rect[1][0] * rect[1][1])
         if area > 5:
             center = (int(rect[0][0]), int(rect[0][1]))
             k = center
             cv2.drawContours(image, [box], 0, (255, 0, 0), 2)
             cv2.circle(image,center,2,(0,255,0),1)
             print(center, a11,a12,a13,a14)

             if center[0] > a11 and center[0] < a13 and center[1] > a12 and center[1] < a14:
                 cv2.putText(image, "in zone a1", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars','right')

             elif center[0] > a21 and center[0] < a23 and center[1] > a22 and center[1] < a24:
                 cv2.putText(image, "in zone a2", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars', 'forward')

             elif center[0] > a31 and center[0] < a33 and center[1] > a32 and center[1] < a34:
                 cv2.putText(image, "in zone a3", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars','right')

             elif center[0] > b11 and center[0] < b13 and center[1] > b12 and center[1] < b14:
                 cv2.putText(image, "in zone b1", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars','right')

             elif center[0] > b21 and center[0] < b23 and center[1] > b22 and center[1] < b24:
                 cv2.putText(image, "in zone b2", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars','forward')

             elif center[0] > b31 and center[0] < b33 and center[1] > b32 and center[1] < b34:
                 cv2.putText(image, "in zone b3", center, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                 client.publish('syssmtcars', 'right')
             else:
                 client.publish('syssmtcars', 'forward')
    #TODO
    print(a11, a12, a13, a14)
    cv2.rectangle(image, (a11,a12), (a13,a14), (255, 0, 0))
    #cv2.rectangle(image, (133,-50), (233,50), (0, 0, 255))
    cv2.rectangle(image, (a21,a22), (a23,a24), (255, 0, 0))
    cv2.rectangle(image, (a31,a32), (a33, a34), (255, 0, 0))
    cv2.rectangle(image, (b11, b12), (b13, b14), (255, 0, 0))
    cv2.rectangle(image, (b21, b22), (b23, b24), (255, 0, 0))
    cv2.rectangle(image, (b31, b32), (b33, b34), (255, 0, 0))

    center_a1 = (int((a13 - a11) / 2) + a11, int((a24 - a12) / 2) + a12)
    center_a2 = (int((a23 - a21) / 2) + a21, int((a24 - a22) / 2) + a22)
    center_a3 = (int((a33-a31)/2)+a31,int((a34-a32)/2)+a32)
    center_b1 = (int((b13 - b11) / 2) + b11, int((b14 - b12) / 2) + b12)
    center_b2 = (int((b23 - b21) / 2) + b21, int((b24 - b22) / 2) + b22)
    center_b3 =(int((b33-b31)/2)+b31,int((b34-b32)/2)+b32)

    cv2.putText(image, "a1", center_a1, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2,2)
    cv2.putText(image, "a2", center_a2, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "a3", center_a3, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b1", center_b1, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b2", center_b2, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b3", center_b3, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)

    cv2.imshow("mask", mask)
    cv2.imshow("original", image)

    if cv2.waitKey(1) == 27:
        break
'''''
a1 - right 
a2 - right 
b1 - right 
b2 - right 

'''''

