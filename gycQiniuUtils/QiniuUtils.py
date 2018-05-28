from qiniu import Auth, put_file, BucketManager
import requests


class qiniuutils:
    def __init__(self):
        accesskey = "vMFonW8ziaY1wOJJJsUCfQGUbs4nGzUs6XT-5rv_"
        secretkey = "WRQzm9pGSQpNrzjNmL9o8AVdtE-ynU7BmUrLDbxe"
        self.auth = Auth(accesskey, secretkey)
        self.bucketname = "gycimgprocess"
        self.fileurl="http://p7dagdk2k.bkt.clouddn.com/"

    def upload(self,filename,filepath):
        '''

        :param filename:上传的文件名
        :param filepath: 本地路径
        :return:
        '''
        bucketname=self.bucketname
        token=self.auth.upload_token(bucketname,key=filename)
        retdata,respinfo=put_file(token,filename,filepath)
        if retdata is not None:
            return retdata['key']
        else:
            print("upload failed")
            return None

    def download(self,key,path="tmp.jpg"):
        fileurl=self.fileurl+key
        r = requests.get(fileurl)
        content = r.content
        with open(path, 'wb') as file:
            file.write(content)
            file.close()
        print("已经保存文件到{}".format(path))

    def delete(self, filename):
        bucket = BucketManager(self.auth)
        reform, fo = bucket.delete(self.bucketname, filename)
        if reform != None:
            print('已经成功地将删除'.format(filename))
        else:
            print('这里出现了一个小错误.(可能是空间并没有这个文件)')
