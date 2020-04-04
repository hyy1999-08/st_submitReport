from flask import Flask, render_template, json, request, send_from_directory, jsonify
import os
from MYDB import MyDBHelper
import  time
import jinja2
import sqlite3
import collections
app = Flask(__name__)

UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER#设置文件上传的目标文件夹
basedir=os.path.abspath(os.path.dirname(__file__))#可以获取当前py文件所在路径
ALLOWED_EXTENSIONS= set(['doc','docx', 'txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])  # 允许上传的文件后缀

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/gohome')
def go_home():
    return render_template("home.html")

#上传word文件功能页面
@app.route('/goshenhe',methods=['GET','POST'])
def go_shenhe():

    return render_template("shenhe.html")

@app.route("/download/",methods=['GET','POST'])
def downloader():
    get_val = request.args.get('stname')
    stname = get_val.split('--', 1)[0]
    username=request.args.get('user')
    myfileorder=request.args.get('myfileorder')
    db=MyDBHelper()
    args=(username,stname)
    row=db.addshenhetn(args)
    sargs=(stname,myfileorder)
    filename=db.getfilename(sargs)[0][4]
    if row>0 :#row>0即返回的是影响行数，而如果返回数组.__length__!=0
        dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
@app.route("/historydownload/",methods=['GET','POST'])
def h_downloader():
    get_val = request.args.get('stname')
    stname = get_val.split('--', 1)[0]
    username=request.args.get('user')
    myfileorder=request.args.get('myfileorder')
    db=MyDBHelper()
    sargs=(stname,myfileorder)
    filename=db.getfilename(sargs)[0][4]
    dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

@app.route('/api/upload',methods=['POST'],strict_slashes=False)#strict_slashes=False对url的/最后的符号是否按个
def api_upload():
    file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER'])#拼接成合法文件夹地址

    if not os.path.exists(file_dir) :
        os.makedirs(file_dir)#文件加不在就创建
    username = request.args.get('user')
    myorder=request.args.get('myorder')
    f=request.files['myfile']#使f称为接受到的对象
    if f and allowed_file(f.filename):
        fname=f.filename
        ext=fname.rsplit('.',1)[1]#获取文件后缀名
        unix_time=int(time.time())
        new_filename=str(unix_time)+'.'+ext
        db=MyDBHelper()
        print(myorder)
        print(type(myorder))
        urealname=db.getshenhern(username)[0]
        args = (username, new_filename, myorder,urealname)
        row=db.addshenhefile(args)
        if row > 0:
            f.save(os.path.join(file_dir,new_filename))
            list=['上传成功!']
            return render_template("tijiao.html",list=list)
    else:
        list=['上传失败!']
        return render_template("tijiao.html", list=list)
@app.route('/addad',methods=['GET'])
def add_ad():
   user = request.args.get('user')
   myfileorder= int(request.args.get('myfileorder'))
   st="已审核"
   username=user.split('--',1)[0]
   args=(st,username,myfileorder)
   db=MyDBHelper()
   row=db.addaudit(args)
   #commit new_val to database
   if row>0:
        return jsonify({'success':True})
   else:
       return jsonify({'error':True})

@app.route('/delete',methods=['GET'])
def go_delete():
    studentname=request.args.get('stname')
    stname=studentname.split("--",1)[0]
    db = MyDBHelper()
    row =db.deleteuser(stname)
    db.deleteusershenhe(stname)
    if row > 0 :
        return jsonify({'success': True})
    else:
        return jsonify({'error': True})

# app.route('/update_cell')
# def update_row():
#    !!!!!!!
#    db=MyDBHelper()
#    db.modifyst()
#
#    #commit new_val to database
#    return render_template("shenhe.html", list=list)
@app.route('/gothome')
def go_thome():
    return render_template("thome.html")
@app.route('/gotijiao')
def go_tijiao():
    return render_template("tijiao.html")
@app.route('/gohistory',methods=['GET','POST'])
def go_history():
    username=request.args.get('user')
    studentname=request.args.get('stname')
    stname=studentname.split("--",1)[0]
    db=MyDBHelper()
    list=db.getallshenhe(stname)
    print(stname)
    print(list)
    product = collections.namedtuple('history', ['id', 'realname','myaudit','myorder','rowid'])
    return render_template("history.html" ,data=[product(*a,i) for i,a in enumerate(list,1)])

@app.route('/gosthistory',methods=['GET','POST'])
def go_sthistory():

    username=request.args.get('user')
    db=MyDBHelper()
    list=db.getsthistorylist(username)
    print(list)
    product = collections.namedtuple('sthistory', ['id', 'realname','myaudit','myorder','rowid'])
    return render_template("studenthistory.html" ,data=[product(*a,i) for i,a in enumerate(list,1)])


@app.route('/gothomelook')
def go_thomelook():
    db=MyDBHelper()
    list=db.getshenhelist()
    print(type(list))#返回的是一个列表
    product =collections.namedtuple('student',['id','realname','myaudit','myorder','rowid'])
    return render_template("thomelook.html",data=[product(*a,i) for i, a in enumerate(list,1)])
@app.route('/gotmanage')
def go_tmanage():
    db = MyDBHelper()
    list = db.getallstudent()

    product = collections.namedtuple('student', ['id', 'realname','rowid'])
    return render_template("tmanage.html",data=[product(*a,i) for i, a in enumerate(list,1)])


@app.route('/')
def hello_world():
    return  render_template("login.html")
@app.route('/register')
def register_go():
    return  render_template("register.html")
@app.route('/checkName', methods=['GET','POST'])
def check_name():
    username=request.args.get("name")
    db=MyDBHelper()
    username=db.Checkusersame(username)
    if username.__len__()==0:
        result =json.dumps({'result':'ok'})
    else:
        result=json.dumps({'result':'no'})
    return result
@app.route('/logintcheck', methods=['GET','POST'])
def check_tusere():
    username=request.args.get("name")
    password=request.args.get("password")
    db=MyDBHelper()

    name=db.Checktusersame(username)
    if name.__len__()!=0:
        pwd = db.GettPassword(username)
        if (password==pwd):
            result =json.dumps({'result':'ok'})
        else:
            result=json.dumps({'result':'no'})
        return result
    else:
        result = json.dumps({'result': 'no'})
        return  result

@app.route('/logincheck', methods=['GET','POST'])
def check_usere():
    username=request.args.get("name")
    password=request.args.get("password")
    db=MyDBHelper()
    print(username)
    print(password)
    name=db.Checkusersame(username)
    if name.__len__()!=0:
        pwd = db.GetPassword(username)
        if (password==pwd):
            result =json.dumps({'result':'ok'})
        else:
            result=json.dumps({'result':'no'})
        return result
    else:
        result = json.dumps({'result': 'no'})
        return  result

@app.route('/checktName', methods=['GET','POST'])
def check_tname():
    username=request.args.get("name")
    db=MyDBHelper()
    username=db.Checktusersame(username)
    if username.__len__()==0:
        result =json.dumps({'result':'ok'})
    else:
        result=json.dumps({'result':'no'})
    return result
# @app.route('/checkadmit',methods=['GET','POST'])
# def check_admit():
#     username=request.args.get('stname')
#     tusername=request.args.get('user')
#     db = MyDBHelper()
#     args=(tusername,username)
#     row1=db.addshenhetn(args)
#     row2=db.checkfile(args)[0][4]
#     if row1.__len__() != 0 and row2.__len__() != 0:
#          result = json.dumps({'result': 'ok','content':"该学生已提交"})
#     else:
#         result = json.dumps({'result': 'no'})
#     return result
@app.route('/getcontent',methods=['GET','POST'])
def get_content():
    username=request.args.get('name')
    db = MyDBHelper()

    row = db.Gettinform(username)[0][3]
    if row.__len__() != 0:
         result = json.dumps({'result': 'ok','content':"%s"%row})
    else:
        result = json.dumps({'result': 'no'})
    return result
@app.route('/getstudentcontent',methods=['GET','POST'])
def get_scontent():
    username=request.args.get('name')
    db = MyDBHelper()
    print(username)
    tusername=db.Checkusersame(username)[0][5]
    row = db.Gettinform(tusername)[0][3]
    if row.__len__() != 0:
         result = json.dumps({'result': 'ok','content':"%s"%row})
    else:
        result = json.dumps({'result': 'no'})
    return result


@app.route('/addtmessage',methods=['GET','POST'])
def add_tmessage():
    username=request.args.get('name')
    tusername=request.args.get("text")
    realname=request.args.get("realname")
    db = MyDBHelper()
    print(username)
    print(tusername)
    print(realname)
    args=(tusername,username)
    row = db.addtusername(args)
    args2=(realname,username)
    db.addrealname(args2)
    content=db.Gettinform(tusername)[0][3]
    if row > 0:
        return json.dumps({'result': 'ok','content':'%s'%content})
    else:
        return json.dumps({'result': 'no'})


@app.route('/doregister',methods=['GET','POST'])
def register_do():
    username=request.args.get('name')
    password=request.args.get('password')
    db = MyDBHelper()
    args=(username, password)
    print(args)
    row = db.adduser(args)
    if row > 0:
        return json.dumps({'result': 'ok'})
    else:
        return json.dumps({'result': 'no'})

@app.route('/addtext', methods=['GET', 'POST'])
def go_addtext():
    text=request.args.get('text')
    name=request.args.get('name')
    db = MyDBHelper()
    print(text)
    print(name)
    args=(text,name)
    row=db.addtext(args)
    if row > 0:
            return json.dumps({'result': 'ok'})
    else:
            return json.dumps({'result': 'no'})

@app.route('/dotregister', methods=['GET', 'POST'])
def tregister_do():
        username = request.args.get('name')
        password = request.args.get('password')
        db = MyDBHelper()
        args = (username, password)
        print(args)
        row = db.addtuser(args)
        if row > 0:
            return json.dumps({'result': 'ok'})
        else:
            return json.dumps({'result': 'no'})


if __name__ == '__main__':
    app.run()
