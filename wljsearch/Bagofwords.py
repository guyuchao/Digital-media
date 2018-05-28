import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.externals import joblib
import cv2
import os

class BuildDict:

    def ReadPicture(self,path):
        img_list=[]
        filenames=os.listdir(path)
        for filename in filenames:
            file = os.path.join(path, filename)
            img = np.array(Image.open(file))
            img_list.append((img, file))
        return np.array(img_list)

    def GetFeatures(self,img_list):
        sift = cv2.xfeatures2d.SIFT_create()
        des_list=[]
        patches=[]
        for img in img_list:
            path=img[1]
            np_img=img[0]
            kp, des = sift.detectAndCompute(np_img, None)
            des_list.append((path,des))
            patches.extend(des)
        return np.array(patches),des_list

    def GetBestCluster(self,patches):
        x = []
        y = []
        for k in range(5, 300):
            km = KMeans(n_clusters=k, random_state=128)
            t = km.fit(patches)
            x.append(k)
            y.append(t.inertia_)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x, y)
        plt.show()

    def KmeansFeatures(self,patches,des_list,k=75):
        km = KMeans(n_clusters=k, random_state=128)
        t = km.fit(patches)
        centers = t.cluster_centers_
        path=[]
        words=[]
        for des in des_list:
            words_count=np.zeros(centers.shape[0])
            for i in des[1]:
                distances = np.power(np.tile(i, (centers.shape[0], 1)) - centers, 2).sum(axis=1)
                words_count[np.argmin(distances)] += 1
            words_count/=words_count.sum(axis=0)
            words.append(words_count)
            path.append(des[0])
        words=np.array(words)
        #求取逆文件频率
        nbr_occurences = np.sum((words>0) * 1, axis=0)
        idf = np.array(np.log(1.0 * len(path) / (1.0 * nbr_occurences)), 'float32')
        words*=idf
        words = preprocessing.normalize(words, norm='l1')
        joblib.dump((words,path,idf,centers,k), "bow.pkl")

t=BuildDict()
pics=t.ReadPicture('/home/wlj/pic/test1/image.orig')
t1,t2=t.GetFeatures(pics)
t.KmeansFeatures(t1,t2)

