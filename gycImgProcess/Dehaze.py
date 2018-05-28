import cv2
import numpy as np
import copy
from PIL import Image

class Dehaze:
    def _min_filter(self,v,r):
        newimg=np.copy(v)
        w,h=v.shape
        for i in range(0,w):
            for j in range(0,h):
                a1=0 if i-r<0 else i-r
                a2=w-1 if i+r+1>w-1 else i+r+1
                b1 = 0 if j - r < 0 else j - r
                b2 = h - 1 if j + r+1 > h - 1 else j + r+1
                newimg[i][j]=v[a1:a2,b1:b2].min(0).min(0)
        return newimg

    def _guidedfilter(self,I, p, r, eps):#参考论文
        m_I = cv2.boxFilter(I, -1, (r, r))
        m_p = cv2.boxFilter(p, -1, (r, r))
        m_Ip = cv2.boxFilter(I * p, -1, (r, r))
        cov_Ip = m_Ip - m_I * m_p
        m_II = cv2.boxFilter(I * I, -1, (r, r))
        var_I = m_II - m_I * m_I
        a = cov_Ip / (var_I + eps)
        b = m_p - a * m_I
        m_a = cv2.boxFilter(a, -1, (r, r))
        m_b = cv2.boxFilter(b, -1, (r, r))
        #Image.fromarray(255*(m_a * I + m_b)).show()
        return m_a * I + m_b


    def _getV1(self,m, eps, w1, maxV1):
        V1 = np.min(m, 2)
        V1 = self._guidedfilter(V1, self._min_filter(V1, 7), 81, eps)#最小值滤波半径7 引导滤波窗口81
        A = V1.argmax()
        w, h = V1.shape
        row = int(A / w)
        col = A % w
        A=m[row, col].mean()
        V1 = np.minimum(V1 * w1, maxV1)
        return V1, A


    def deHaze(self,imgpath, eps=0.001, w=0.95, maxV1=0.80):
        img=np.array(Image.open(imgpath))/255
        V1, A = self._getV1(img, eps, w, maxV1)  # 得到遮罩图像和大气光照
        newimg=copy.deepcopy(img)
        a,b,_=img.shape
        for i in range(0,a):
            for j in range(0,b):
                newimg[i,j,:]=(img[i,j,:]-A)/max(0.1,1-V1[i][j])+A
        Y = np.clip(newimg, 0, 1)*255
        return Image.fromarray(Y.astype(np.uint8))




#img=Image.open("/home/guyuchao/PycharmProjects/src/gycImgProcess/7.png")
#m = Dehaze().deHaze(img).show()