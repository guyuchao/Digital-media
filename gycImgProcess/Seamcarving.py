import cv2
import numpy as np
from PIL import Image
import copy
from tqdm import tqdm
import imageio
from gycImgProcess.Basicprocess import Basicprocess

class Seamcarving:
    def __init__(self):
        self.progress=0

    def get_progress(self):
        return self.progress

    def _dynamic_programing(self,sobel_img):
        mat=sobel_img.astype(np.int32).copy()
        h, w = sobel_img.shape
        for i in range(1, h):
            for j in range(0, w):
                mat[i][j] += min(mat[i - 1, max(0,j-1):min(j+1,w)])
        return mat

    def _gen_seam(self,dynamic_mat,where=None):
        def argmin(a1,a2,a3):
            if a1<=a2 and a1<=a3:
                return 0
            elif a2<=a1 and a2<=a3:
                return 1
            elif a3<=a1 and a3<=a2:
                return 2
        h,w=dynamic_mat.shape
        bool_mat=np.ones((h,w),dtype=bool)
        if where is None:
            where=np.argmin(dynamic_mat[-1,:])
        bool_mat[-1,where]=False
        for row in range(h-2,-1,-1):
            if where==0:
                if dynamic_mat[row,where]>dynamic_mat[row,where+1]:
                    where+=1
            elif where==w-1:
                if dynamic_mat[row,where]>dynamic_mat[row,where]:
                    where-=1
            else:
                where += argmin(dynamic_mat[row, where - 1],dynamic_mat[row, where ],dynamic_mat[row, where +1]) - 1
            bool_mat[row,where]=False
        return bool_mat

    def _seam_carving(self,img, iter,gif_name=None,gen_gif=False):
        images=[]
        if gen_gif is True:
            assert gif_name is None,"input gif_name"
        for i in tqdm(range(iter)):
            np_img_rgb = np.array(img)
            h,w,c=np_img_rgb.shape
            np_img_grey = np.array(img.convert('L'))
            sobel_img = self._sobel(np_img_grey)
            mat = self._dynamic_programing(sobel_img)
            bool_mat=self._gen_seam(mat)

            if gen_gif is True:
                np_img_rgb_trace=copy.deepcopy(np_img_rgb)
                np_img_rgb_trace[~bool_mat]=255
                Image.fromarray(np_img_rgb_trace.astype(np.uint8)).save("tmp_trace.jpg", format='JPEG')
                img_trace = imageio.imread("tmp_trace.jpg", format='JPEG')
                images.append(img_trace)
            img=Image.fromarray(np_img_rgb[bool_mat].reshape(h,w-1,c).astype(np.uint8))
        if gen_gif is True:
            imageio.mimsave(gif_name, images, duration=0.1)
        img.show()
        return img

    def resize_img(self,img,size,gen_gif=False):
        assert len(size)==2,"size error"
        w,h=img.size
        if w>size[0]:
            if gen_gif is True:
                img=self._seam_carving(img,iter=w-size[0],gif_name="horizontal.gif",gen_gif=True)
            else:
                img = self._seam_carving(img, iter=w - size[0])
        if h>size[1]:
            img = img.transpose(Image.ROTATE_90)
            if gen_gif is True:
                img=self._seam_carving(img,iter=h-size[1],gif_name="vertical.gif",gen_gif=True)
            else:
                img = self._seam_carving(img, iter=h-size[1])
            img=img.transpose(Image.ROTATE_270)
        img.show()
        return img

    def object_remove(self,imgpath,mask):
        img=Image.open(imgpath)
        mask=np.array(mask)
        h,w,c=mask.shape

        remain_bool=np.zeros((h,w))
        remove_bool=np.zeros((h,w))

        remove_r_mask=(mask[:,:,0]>100)
        remove_g_mask=(mask[:,:,1]<50)
        remove_b_mask=(mask[:,:,2]<50)

        remain_r_mask=(mask[:,:,0]<50)
        remain_g_mask = (mask[:, :, 1] > 200)
        remain_b_mask = (mask[:, :, 2] <50)

        remove_bool[remove_r_mask&remove_g_mask&remove_b_mask]=1
        remain_bool[remain_r_mask&remain_g_mask&remain_b_mask]=1

        remove_bool=remove_bool.astype(np.bool)
        remain_bool=remain_bool.astype(np.bool)

        self.total=remove_bool.sum(0).sum(0)+1

        while remove_bool.sum(0).sum(0)>5:
            self.progress = (1-remove_bool.sum(0).sum(0)/self.total)*100
            np_img_rgb = np.array(img)
            h, w, c = np_img_rgb.shape
            np_img_grey = np.array(img.convert('L'))
            sobel_img = self._sobel(np_img_grey).astype(np.int16)
            sobel_img[remove_bool] *= -10
            sobel_img[remain_bool] *= 10
            mat = self._dynamic_programing(sobel_img)
            bool_mat = self._gen_seam(mat)
            remain_bool=remain_bool[bool_mat].reshape(h,w-1)
            remove_bool=remove_bool[bool_mat].reshape(h,w-1)
            img = Image.fromarray(np_img_rgb[bool_mat].reshape(h, w - 1, c).astype(np.uint8))
        self.progress=100
        return img


    def _sobel(self,npimg_grey):
        npimg_grey = cv2.medianBlur(npimg_grey, 5)
        x = cv2.Sobel(npimg_grey, cv2.CV_16S, 1, 0)  #
        y = cv2.Sobel(npimg_grey, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)  # 转回uint8
        absY = cv2.convertScaleAbs(y)
        sobel_img = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        return sobel_img

'''
img_path=Image.open("/home/guyuchao/github/src/gycImgProcess/5.jpg")
se=Seamcarving()

#se.resize_img(img_path,(500,300))
se.seam_carving(img_path,100)
'''
'''
img_path=Image.open("/home/guyuchao/github/src/testttt.jpg")
mask_path=Image.open("/home/guyuchao/github/src/hhhhh.jpg")

se=Seamcarving()

se.object_remove(img_path,mask_path).show()
'''