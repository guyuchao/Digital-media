import numpy as np
from PIL import Image
from scipy import sparse
from scipy.sparse import linalg
import cv2
from gycImgProcess.Basicprocess import Basicprocess

class Colorized:

    def __init__(self):
        self.progress=0

    def get_progress(self):
        return self.progress

    def _rgb2yuv(self,rgbimg):
        return cv2.cvtColor(rgbimg,cv2.COLOR_RGB2YUV)

    def _yuv2rgb(self,yuvimg):
        return cv2.cvtColor(yuvimg,cv2.COLOR_YUV2RGB)

    def colorize(self,imgpath,mark):
        #path_greyimg="/home/guyuchao/github/src/gycImgProcess/example2.bmp"
        #path_mask="/home/guyuchao/github/src/testimg.jpg"
        original = np.array(Image.open(imgpath).resize((400, 400)))
        neworiginal=np.zeros((original.shape[0],original.shape[1],3))
        if len(original.shape)==2:#单通道灰度图
            neworiginal[:,:,0]=original
            neworiginal[:,:,1]=original
            neworiginal[:,:,2]=original
            original=neworiginal.astype(np.uint8)
        #original=np.array(Image.open(imgpath))
        marked=np.array(mark)
        isColored=((marked[:,:,0]>20) | (marked[:,:,1]>20) |(marked[:,:,2]>20))
        yuv_origin=self._rgb2yuv(original)
        yuv_mark=self._rgb2yuv(marked)
        #isColored = abs(original - marked).sum(2) > 2.55 # isColored as colorIm
        YUV=np.zeros((original.shape))
        YUV[:, :, 0] = yuv_origin[:,:,0]
        YUV[:, :, 1] = yuv_mark[:,:,1]
        YUV[:, :, 2] = yuv_mark[:,:,2]
        h ,w,_= YUV.shape
        image_size = h * w

        order = np.arange(image_size).reshape(h, w, order='F').copy()
        around_num=9
        max_matrix_len = image_size * around_num
        row_inds = np.zeros(max_matrix_len, dtype=np.int64)
        col_inds = np.zeros(max_matrix_len, dtype=np.int64)
        vals = np.zeros(max_matrix_len)

        inds_length = 0  # 稀疏索引长度
        pixel_where = 0  # 像素所在位置
        for j in range(w):
            self.progress=100*j/w if 100*j/w<95 else 95
            for i in range(h):
                if (not isColored[i, j]):
                    window_index = 0
                    window_vals = np.zeros(around_num)

                    for ii in range(max(0, i - 1), min(i +2, h)):
                        for jj in range(max(0, j - 1), min(j + 2, w)):
                            if (ii != i or jj != j):
                                row_inds[inds_length] = pixel_where
                                col_inds[inds_length] = order[ii, jj]
                                window_vals[window_index] = YUV[ii, jj, 0]
                                inds_length += 1
                                window_index += 1

                    center = YUV[i, j, 0].copy()  # t_val as center
                    window_vals[window_index] = center

                    variance=np.var(window_vals[0:window_index+1])
                    sigma = variance * 0.6

                    mgv = min((window_vals[0:window_index + 1] - center) ** 2)
                    if (sigma < (-mgv / np.log(0.01))):
                        sigma = -mgv / np.log(0.01)
                    if (sigma < 0.000002):
                        sigma= 0.000002

                    window_vals[0:window_index] = np.exp(
                        -((window_vals[0:window_index] - center) ** 2) / (sigma))
                    window_vals[0:window_index] = window_vals[0:window_index] / np.sum(
                        window_vals[0:window_index])
                    vals[inds_length - window_index:inds_length] = -window_vals[0:window_index]

                row_inds[inds_length] = pixel_where
                col_inds[inds_length] = order[i, j]
                vals[inds_length] = 1
                inds_length+= 1
                pixel_where += 1
        vals = vals[0:inds_length]
        col_inds = col_inds[0:inds_length]
        row_inds = row_inds[0:inds_length]
        A = sparse.csr_matrix((vals, (row_inds, col_inds)), (pixel_where, image_size))
        b = np.zeros((A.shape[0]))

        colorized = np.zeros(YUV.shape)
        colorized[:, :, 0] = YUV[:, :, 0]

        color_copy_for_nonzero = isColored.reshape(image_size,order='F').copy()
        colored_inds = np.nonzero(color_copy_for_nonzero)
        for t in [1, 2]:
            curIm = YUV[:, :, t].reshape(image_size, order='F').copy()
            b[colored_inds] = curIm[colored_inds]
            new_vals = linalg.spsolve(A,b)
            colorized[:, :, t] = new_vals.reshape(h, w, order='F')
        self.progress=100
        return Image.fromarray(self._yuv2rgb(colorized.astype(np.uint8)))
'''
imgpath="/home/guyuchao/github/src/gycImgProcess/example2.bmp"
mask=Image.open("/home/guyuchao/github/src/testimg.jpg")
Colorized().colorize(imgpath,mask).show()
'''