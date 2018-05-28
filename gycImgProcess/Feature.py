import cv2 as cv
from matplotlib import pyplot as plt
#读取需要特征匹配的两张照片，格式为灰度图。
img1=cv.imread("image/4444.jpg",0)
img2=cv.imread("image/3333.jpg",0)
orb=cv.ORB_create()#建立orb特征检测器
kp1,des1=orb.detectAndCompute(img1,None)#计算img1中的特征点和描述符
kp2,des2=orb.detectAndCompute(img2,None) #计算img2中的
bf = cv.BFMatcher(cv.NORM_HAMMING,crossCheck=True) #建立匹配关系
mathces=bf.match(des1,des2) #匹配描述符
mathces=sorted(mathces,key=lambda x:x.distance) #据距离来排序
img3=cv.drawMatches(img1,kp1,img2,kp2,mathces[:40],2) #画出匹配关系
plt.imshow(img3),plt.show() #matplotlib描绘出来