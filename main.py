# encoding=utf-8
from flask import Flask, request,jsonify,session
from flask_uploads import UploadSet, configure_uploads
from flask import render_template
import os
import base64
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from gycMysqlUtils.model import User,Img,UserImg
from io import BytesIO

from wljsearch.SearachImage import searchimage
from gycImgProcess.Basicprocess import Basicprocess
from gycImgProcess.Filtering import Filtering
from gycImgProcess.Seamcarving import Seamcarving
from gycImgProcess.Colorized import Colorized
from gycImgProcess.Dehaze import Dehaze
from gycOsUtils.osUtils import osutils
from gycQiniuUtils.QiniuUtils import qiniuutils

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:guyuchao@127.0.0.1:3306/imgprocess'#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True #实例化
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

app.config['SECRET_KEY']="lovewlj"

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)),"files")
app.config['UPLOADS_DEFAULT_DEST'] = os.path.dirname(os.path.abspath(__file__))
uploaded_photos = UploadSet()
configure_uploads(app, uploaded_photos)


'''
img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_search'))
    imgpathlist=searchimage().GetImageFeature(img_path)
    img_url = {"code": 200, "len": 7}
    for idx,path in enumerate(imgpathlist):
        img_url['img'+str(idx)]=Basicprocess().img2base64(Image.open(path))
    return jsonify(img_url)

'''
@app.route('/')
def index():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        return render_template('foundation.html')

@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        username = request.form['form-username']
        password = request.form['form-password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.password==password:
            session['username']=username
            session['userid']=user.userid
            return render_template("foundation.html")
        else:
            return render_template("register.html")


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['form-username']
        password=request.form['form-password']
        user=User(username,password)
        db.session.add(user)
        #db.session.commit()
        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route('/workplace',methods=['GET'])
def workplace():
    return render_template("thumbnail.html")

@app.route('/search',methods=['GET'])
def search():
    return render_template("search.html")

@app.route('/thumbnail',methods=['GET'])
def thumbnail():
    #get userid
    userid=session.get('userid')
    #userid=2
    file_url=qiniuutils().fileurl
    userimgli = UserImg.query.filter_by(userid=userid).all()
    img_url={"code":200,"len":len(userimgli)}
    for idx,userimg in enumerate(userimgli):
        img_url['img'+str(idx)]=file_url+userimg.filename+'-imgthumbnail'
    print(img_url)
    return jsonify(img_url)

@app.route('/searchimg',methods=['GET'])
def searchimg():
    '''
    #img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_search'))
    #imgpathlist=.GetImageFeature('../205.jpg')

    img_url = {"code": 200, "len": 7}
    for i in range(7):
        imgpath='files/wanglijuan/searchpath/'+str(i)+'.jpg'

        img_url['img'+str(i)]=Basicprocess().img2base64(Image.open(imgpath))
    return jsonify(img_url)
    '''
    if session.get('handlingfile_search') is not None:
        img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_search'))
        imgpathlist = searchimage().GetImageFeature(img_path)
        img_url = {"code": 200, "len": 7}
        for idx, path in enumerate(imgpathlist):
            img_url['img' + str(idx)] = Basicprocess().img2base64(Image.open(path))
        return jsonify(img_url)
    else:
        return jsonify({'code': 404})

@app.route('/dehazepage')
def dehazepage():
    return render_template("dehaze.html")


@app.route('/filter')
def filter():
    return render_template('filter.html')

@app.route('/seamcarving')
def seamcarving():
    return render_template('objectremove.html')

@app.route('/colorize')
def colorize():
    return render_template('colorizer.html')

@app.route('/dehaze',methods=['POST'])
def dehaze():
    if session.get('handlingfile_dehaze') is not None:
        img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_dehaze'))
        img = Dehaze().deHaze(img_path)
        #buffered = BytesIO()
        #img.save(buffered, format="PNG")
        #img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        session['handlingfile_dehaze_tmp'] = osutils().add_tmp_in_filename(session.get('handlingfile_dehaze'))
        img.save(os.path.join(app.config['UPLOAD_PATH'], session['handlingfile_dehaze_tmp']), format="PNG")
        img_str = Basicprocess().img2base64(img)
        return jsonify({'code': 200, 'img64': img_str})
    else:
        return jsonify({'code': 404})


se=Seamcarving()

@app.route('/seamcarving/seamcarver', methods=['POST','GET'])
def seamcarver():
    if request.method=='POST':
        if session.get('handlingfile_objectremove') is not None:
            imgbase64 =request.values.get('image').split(",")[1]
            #basicprocess=Basicprocess()
            mask=Basicprocess().base64_to_rgb(imgbase64)
            img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_objectremove'))
            img=se.object_remove(img_path,mask)
            #buffered = BytesIO()
            #mg.save(buffered, format="PNG")
            #img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            session['handlingfile_objectremove_tmp'] = osutils().add_tmp_in_filename(session.get('handlingfile_objectremove'))
            img.save(os.path.join(app.config['UPLOAD_PATH'], session['handlingfile_objectremove_tmp']), format="PNG")
            img_str = Basicprocess().img2base64(img)
            return jsonify({'code': 200, 'img64': img_str})
        else:
            return jsonify({'code': 404})
    if request.method=='GET':
        return jsonify({'code': 0, 'progress': se.get_progress()})
cl=Colorized()

@app.route('/colorize/colorizer', methods=['POST','GET'])
def colorizer():
    if request.method=='POST':
        if session.get('handlingfile_colorizer') is not None:
            imgbase64 =request.values.get('image').split(",")[1]
            #basicprocess=Basicprocess()
            mark=Basicprocess().base64_to_rgb(imgbase64)
            img_path = os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_colorizer'))
            img=cl.colorize(img_path,mark)
            #buffered=BytesIO()
            #img.save(buffered, format="PNG")
            #img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            session['handlingfile_colorizer_tmp'] = osutils().add_tmp_in_filename(session.get('handlingfile_colorizer'))
            img.save(os.path.join(app.config['UPLOAD_PATH'], session['handlingfile_colorizer_tmp']), format="PNG")
            img_str = Basicprocess().img2base64(img)
            return jsonify({'code': 200, 'img64': img_str})
        else:
            return jsonify({'code': 404})
    if request.method=='GET':
        return jsonify({'code': 0, 'progress': cl.get_progress()})


@app.route('/upload/<string:method>', methods=['POST'])
def flask_upload(method):
    '''

    :param method:basicprocess filter colorizer objectremove
    :return:
    '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                filename = uploaded_photos.save(file,folder=session.get('username'))
                str="handlingfile_"+method
                session[str]=filename

                #print(str)
                return jsonify({'code': 0, 'filename': filename, 'msg': uploaded_photos.url(filename)})
            except Exception as e:
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})

# show photo
@app.route('/files/<string:method>', methods=['GET'])
def show_photo(method):
    if request.method == 'GET':
        str="handlingfile_"+method
        if session.get(str) is not None:
            #buffer=BytesIO()
            print(os.path.join(app.config['UPLOAD_PATH'],session.get(str)))
            img=Image.open(os.path.join(app.config['UPLOAD_PATH'],session.get(str)))
            img=img.resize((400,400))
            #img.save(buffer,'PNG')
            img.save(os.path.join(app.config['UPLOAD_PATH'],session.get(str)),'PNG')
            #img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            img_str = Basicprocess().img2base64(img)
            return jsonify({'code': 200, 'img64': img_str})
        else:
            return jsonify({'code':404})

@app.route('/save/<string:method>',methods=['POST'])
def save(method):
    session_item="handlingfile_"+method+"_tmp"
    if session.get(session_item) is not None:
        filename=session.get(session_item)
        img=Img(filename)
        db.session.add(img)
        db.session.commit()

        upload_filename=str(session.get('userid'))+'_'+str(img.imgid)+osutils().get_extension(filename)
        upload_path=os.path.join(app.config['UPLOAD_PATH'],session[session_item])
        qiniuutils().upload(upload_filename,upload_path)

        userimg=UserImg(userid=session.get('userid'),imgid=img.imgid,filename=upload_filename)
        db.session.add(userimg)
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code':404})

@app.route('/basicprocess/<string:method>',methods=['POST'])
def basicprocess(method):
    if session.get('handlingfile_basicprocess') is not None:
        radio = request.form[method]
        img_path=os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_basicprocess'))
        #basic_process =
        #buffered = BytesIO()
        if method=="contrast":
            img=Basicprocess().change_contrast(img_path,float(radio))
        elif method=="value":
            img = Basicprocess().change_value_quick(img_path,float(radio))
        elif method=="saturation":
            img = Basicprocess().change_saturation_quick(img_path,float(radio))
        elif method == "hue":
            img = Basicprocess().change_hue_quick(img_path,float(radio))


        session['handlingfile_basicprocess_tmp']=osutils().add_tmp_in_filename(session.get('handlingfile_basicprocess'))
        img.save(os.path.join(app.config['UPLOAD_PATH'],session['handlingfile_basicprocess_tmp']),format="PNG")
        #img.save(buffered, format="PNG")
        #img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        img_str=Basicprocess().img2base64(img)
        return jsonify({'code': 200, 'img64': img_str})
    else:
        return jsonify({'code': 404})


@app.route('/filtering/<string:method>',methods=['POST'])
def filtering(method):
    if session.get('handlingfile_filter') is not None:
        img_path=os.path.join(app.config['UPLOAD_PATH'], session.get('handlingfile_filter'))
        filtering = Filtering(img_path)
        #buffered = BytesIO()
        if method=="mean-filter":
            img=filtering.mean_filter()
        elif method=="median-filter":
            img=filtering.median_filter()
        elif method=="gaussian-filter":
            img=filtering.gaussian_filter()
        elif method=="bilateral-filter":
            img=filtering.bilateral_filter()

        session['handlingfile_filter_tmp']=osutils().add_tmp_in_filename(session.get('handlingfile_filter'))
        img.save(os.path.join(app.config['UPLOAD_PATH'],session['handlingfile_filter_tmp']),format="PNG")


        img_str = Basicprocess().img2base64(img)

        return jsonify({'code': 200, 'img64': img_str})
    else:
        return jsonify({'code': 404})

@app.route('/clear',methods=['POST'])
def clear():
    if session.get('handlingfile') is not None:
        img_path = os.path.join(app.config['UPLOAD_PATH'], 'files/%s' % session.get('handlingfile'))
        img_str = base64.b64encode(open(img_path, "rb").read()).decode('utf-8')
        return jsonify({'code': 200, 'img64': img_str})
    else:
        return jsonify({'code': 404})

@app.route('/noise/<string:method>',methods=['POST'])
def noise(method):
    if session.get('handlingfile') is not None:
        img_path = os.path.join(app.config['UPLOAD_PATH'], 'files/%s' % session.get('handlingfile'))
        filtering = Filtering(img_path)
        buffered = BytesIO()
        if method=="salt_noise":
            img=filtering.salt_noise()
        elif method=="gaussian_noise":
            img=filtering.gaussian_noise()
        session['handlingfile']=os.path.splitext(session.get('handlingfile'))[0]+method+os.path.splitext(session.get('handlingfile'))[1]
        new_img_path = os.path.join(app.config['UPLOAD_PATH'], 'files/%s' % session.get('handlingfile'))
        img.save(new_img_path)
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(open(img_path, "rb").read()).decode('utf-8')
        return jsonify({'code': 200, 'img64': img_str})
    else:
        return jsonify({'code': 404})

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4400, threaded=True)