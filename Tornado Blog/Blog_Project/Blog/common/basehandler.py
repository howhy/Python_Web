#-*- coding:utf-8 -*-
import hashlib
import tornado.websocket
import tornado.web
from pycket.session import SessionMixin
from Blog.user.usermodel import User
from webblog_app.models import UploadFile,hash_data
from dbhandler import DBHandler, DBsession
from validation_code import gene_code
from validation_code import gen_qrcode
from Blog.settings import setting
from Blog.common.pagination import PaginationHandler
import os

class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    """
    *RequestHandler SessionMixin基类*
    """
    def get_current_user(self):
        user=self.session.get("username",None)
        user_obj=DBHandler(User,User.name).query(user)[0] if user else None
        return user_obj if user_obj else None

    def auth_password(self,pwd):
        hasobj = hashlib.md5("woshishui")
        hasobj.update(pwd)
        return hasobj.hexdigest()
   
   # def write_error(self, status_code, **kwargs):
   #     if status_code == 404:
   #         self.render('404.html')
   #     elif status_code == 500:
   #         self.render('500.html')
   #     else:
   #         super(BaseHandler, self).write_error(status_code, **kwargs)

    def on_finish(self):
        DBsession.close()

class CheckCodeHandler(BaseHandler):
    """
    *验证码手动更新*
    """
    def get(self):
        code,stream=gene_code()
        self.session.set('code', code)
        self.write(stream.getvalue())
class QRCodeHandler(BaseHandler):
    """
    *网站二维码生成*
    """
    @tornado.web.authenticated
    def get(self):
        stream = gen_qrcode('%s/%s.html'%(self.request.host,self.current_user.name), '%s/%s' % (setting['static_path'], self.current_user.image))
        self.write(stream.getvalue())

class UploadFileHandler(BaseHandler):
    """
    上传文件
    """
    @tornado.web.authenticated
    def post(self):
        upload_file=self.request.files.get('fileinput')
        for files in upload_file:
            file_size=len(files['body'])
            file_name=files['filename']
            file_type = files['content_type']
            file_path = '%s/%s/%s' % (setting['static_path'], 'upload', file_name)
            file_obj = DBHandler(UploadFile, UploadFile._file_hash).query(hash_data(files['body']))
            if os.path.splitext(file_name)[1] not in ['.conf','.zip', '.rar',  '.css', '.xml','.png','.jpg','.jpeg', '.7z', '.ico', '.pdf' ,'.ppt' ,'.pptx' , '.xls' ,'.doc' ,'.log', '.txt',  '.gif', '.tar' , '.gz','.docx','.xlsx','.bmp']:
                msg = "文件类型不允许"
                ret = {'error': 1, 'url': '/static/upload/%s' % file_name, 'message': msg}
                return self.write(ret)
            elif file_size>2048000:
                msg = "文件大小大于2M"
                ret = {'error': 1, 'url': '/static/upload/%s' % file_name, 'message': msg}
                return self.write(ret)
            elif not file_obj:
                 with open(file_path,'wb') as f:
                      f.write(files['body'])
                 save_file=UploadFile(filename=file_name,file_type=file_type,filesize=file_size,file_hash=files['body'],user_id=self.current_user.id)
                 DBHandler(save_file).add()
                 msg='上传成功'
                 ret = {'error': 0, 'url': '/static/upload/%s' % file_name, 'message': msg}
                 return self.write(ret)

            else:
                 msg='文件已存在'
                 ret = {'error': 1, 'url': '/static/upload/%s' % file_name, 'message': msg}
                 return self.write(ret)



class DownloadFileHandler(BaseHandler):
    """
    下载文件
    """
    def get(self):
        file_obj = DBHandler(UploadFile,UploadFile.id).query(self.get_argument('id', ''))[0]
        file_path = '%s/%s/%s' % (setting['static_path'], 'upload', file_obj.filename)
        if file_obj:
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' +file_obj.filename)
            with open(file_path, 'rb') as f:
                while 1:
                    data = f.read(2048)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        else:
            self.write('no filename')




class BaseWebSocket(tornado.websocket.WebSocketHandler, SessionMixin):
    def get_current_user(self):
        user = self.session.get("username",None)
        user_obj = DBHandler(User, User.name).query(user)[0] if user else None
        return user_obj if user_obj else None
