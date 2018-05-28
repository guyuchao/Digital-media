from PIL import Image
import numpy as np
import random

class Filtering:
    def __init__(self,imgpath):
        self._imgpath=imgpath
        img = Image.open(self._imgpath).convert('RGB')
        self.npimg=np.array(img)

    def gaussian_noise(self,mean=0,sigma=40):
        noise=np.random.normal(mean,sigma,self.npimg.shape)
        newimg=self.npimg+noise
        newimg[newimg>255]=255
        newimg[newimg<0]=0
        return Image.fromarray(newimg.astype(np.uint8))

    def salt_noise(self,percent=0.03):
        w,h,_=self.npimg.shape
        newimg=np.copy(self.npimg)
        for i in range(int(w*h*percent)):
            newimg[random.randint(0,w-1),random.randint(0,h-1)]=255*random.randint(0,1)
        return Image.fromarray(newimg.astype(np.uint8))


    def mean_filter(self):
        newimg=np.copy(self.npimg)
        w,h,_=newimg.shape
        for i in range(1,w-1):
            for j in range(1,h-1):
                newimg[i][j][:]=self.npimg[i-1:i+2,j-1:j+2].mean(axis=0).mean(axis=0)
        return Image.fromarray(newimg.astype(np.uint8))

    def min_filter(self):
        newimg=np.ones(self.npimg.shape[:2])
        w,h,_=self.npimg.shape
        for i in range(0,w):
            for j in range(0,h):
                newimg[i][j]=np.min(self.npimg[i][j])
        print(newimg)
        newimg2=np.copy(newimg)
        for i in range(0,w):
            for j in range(0,h):
                a1=0 if i-7<0 else i-7
                a2=w-1 if i+8>w-1 else i+8
                b1 = 0 if j - 7 < 0 else j - 7
                b2 = h - 1 if j + 8 > h - 1 else j + 8
                newimg2[i][j]=newimg[a1:a2,b1:b2].min(0).min(0)
        newimg2=255-newimg2
        return Image.fromarray(newimg2.astype(np.uint8))

    def min_filter2(self):
        newimg=np.ones(self.npimg.shape[:2])
        w,h,_=self.npimg.shape
        for i in range(0,w):
            for j in range(0,h):
                newimg[i][j]=np.min(self.npimg[i][j])
        newimg2=np.copy(newimg)
        for i in range(0,w):
            for j in range(0,h):
                a1=0 if i-7<0 else i-7
                a2=w-1 if i+8>w-1 else i+8
                b1 = 0 if j - 7 < 0 else j - 7
                b2 = h - 1 if j + 8 > h - 1 else j + 8
                newimg2[i][j]=newimg[a1:a2,b1:b2].min(0).min(0)
        A =140
        newimg2=(255-newimg2)/A
        newimg3=np.copy(self.npimg)


        for i in range(0,w):
            for j in range(0,h):
                #print(self.npimg[i,j:])
                newimg3[i,j,:]=((self.npimg[i,j,:]-A)/max(newimg2[i,j],0.3))+A
        newimg3[newimg3>255]=255
        newimg3[newimg3<0]=0

        return Image.fromarray(newimg3.astype(np.uint8))

    def median_filter(self):
        newimg=np.copy(self.npimg)
        w,h,_=newimg.shape
        for i in range(1,w-1):
            for j in range(1,h-1):
                newimg[i][j][:]=np.sort(self.npimg[i-1:i+2,j-1:j+2,0].flatten())[4],np.sort(self.npimg[i-1:i+2,j-1:j+2,1].flatten())[4],np.sort(self.npimg[i-1:i+2,j-1:j+2,2].flatten())[4]
        return Image.fromarray(newimg.astype(np.uint8))

    def _gen_gaussian_kernel(self,size, sigma):
        kernel = np.zeros((size, size))
        center = (size - 1) / 2
        for i in range(0, size):
            for j in range(0, size):
                kernel[i][j] = np.exp(-(np.power(i - center, 2) + np.power(j - center, 2)) / (2 * sigma * sigma)) / (2 * np.pi * sigma * sigma)
        kernel = (kernel / kernel[0][0]).astype(np.int)
        coefficient = kernel.sum()
        kernel = kernel[:, :, np.newaxis]
        kernel = np.repeat(kernel, 3, axis=2)
        return kernel, coefficient

    def gaussian_filter(self,):
        kernel,coefficient=self._gen_gaussian_kernel(3,0.8)
        w,h,_=self.npimg.shape
        newimg=np.copy(self.npimg)
        for i in range(1,w-1):
            for j in range(1,h-1):
                newimg[i][j]=(self.npimg[i-1:i+2,j-1:j+2]*kernel/coefficient).sum(axis=0).sum(axis=0)
        return Image.fromarray(newimg.astype(np.uint8))


    def _gen_gaussian_kernel_bilateral(self, sigma):
        kernel = np.zeros((3, 3))
        center = (3 - 1) / 2
        for i in range(0, 3):
            for j in range(0, 3):
                kernel[i][j] = np.exp(-(np.power(i - center, 2) + np.power(j - center, 2)) / (2 * sigma * sigma))
        kernel /= kernel.sum()
        return kernel

    def bilateral_filter(self,sigma1=0.8,sigma2=1):
        kernel= self._gen_gaussian_kernel_bilateral(sigma1)
        #print(kernel[:,:,0])
        w, h, _ = self.npimg.shape
        newimg = np.copy(self.npimg)
        for i in range(1,w-1):
            for j in range(1,h-1):
                img=self.npimg[i-1:i+2,j-1:j+2,:]
                img_center=self.npimg[i,j,:]
                r = np.power(img[:, :, 0] - img_center[0], 2)
                g = np.power(img[:, :, 1] - img_center[1], 2)
                b = np.power(img[:, :, 2] - img_center[2], 2)
                H=np.exp((r+g+b)/(-2*sigma2*sigma2))
                W=np.dot(kernel,H)
                W/=W.sum()
                newimg[i][j][0]=np.sum(W*img[:,:,0])
                newimg[i][j][1]=np.sum(W*img[:,:,1])
                newimg[i][j][2]=np.sum(W*img[:,:,2])
        return Image.fromarray(newimg.astype(np.uint8))
