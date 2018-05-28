from PIL import Image
import numpy as np

class Imagemerge:


    def merge(self,img1,img2,alpha):
        assert alpha>=0 and alpha<=1,"alpha should be （0,1)"
        img1=np.array(img1)
        img2=np.array(img2)
        ret_img=img1*(1-alpha)+img2*alpha
        return Image.fromarray(ret_img.astype(np.uint8))


path1="/home/guyuchao/github/src/static/img/1.jpg"
path2="/home/guyuchao/github/src/test2.jpg"

im=Imagemerge(path1,path2)
im.merge(0.3).show()