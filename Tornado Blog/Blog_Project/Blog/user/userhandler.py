#-*- coding:utf-8 -*-
from Blog.common.dbhandler import DBHandler
from Blog.common.basehandler import BaseHandler
from Blog.common.validation_code import gene_code
from usermodel import User,uuid4
import datetime
import itchat
import tornado.web
class EnrollHandler(BaseHandler):
    """
    *注册页面处理*
    """
    def get(self):
        self.render('enroll.html',errinfo=None)
    def post(self):
        username=self.get_argument('username',None)
        password=self.get_argument('password',None)
        confirmpassword=self.get_argument('confirmpassword',None)
        email=self.get_argument('email',None)
        if username and password and email and confirmpassword:
            query_user=DBHandler(User,User.name).query(username)
            if not query_user:
                if password==confirmpassword:
                    user1=User(id=str(uuid4()),name=username,password=self.auth_password(password),email=email)
                    DBHandler(user1).add()
                    self.redirect('login')
                else:
                    self.render('enroll.html', errinfo=u'*两次密码不一样*')
            else:
                self.render('enroll.html',errinfo=u'*用户%s已经存在*'%username)
        else:
            self.render('enroll.html', errinfo=u'*所有字段不允许为空*')
class LoginHandler(BaseHandler):
    """
       *登入页面处理*
       """
    def get(self,err_info=None):
        code,stream= gene_code()
        self.session.set('code', code)
        self.render('login.html', errinfo=err_info)

    def post(self):
        username = self.get_argument("username",None)
        password = self.get_argument("password",None)
        code = self.get_argument("code",None)
        errinfo = ""
        getcode=self.session.get('code')
        if username and password and code and getcode:
            if code.upper() == getcode.upper():
                userobj = DBHandler(User, User.name).query(username)
                if userobj:
                    if userobj[0].password == self.auth_password(password):
                        userobj[0].logintime=current_time=current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        DBHandler(User).commit()
                        self.session.set("username", username)
                        prevurl = self.get_argument("prevurl") if self.get_argument("prevurl") else "/%s.html"%username
                        self.redirect(prevurl)
                    else:
                        errinfo = "密码错误"
                        self.get(err_info=errinfo)
                else:
                    errinfo = "用户名不存在"
                    self.get(err_info=errinfo)
            else:
                errinfo = "验证码错误"
                self.get(err_info=errinfo)
        else:
            self.get(err_info="用户名 密码不能为空")

class LogoutHandler(BaseHandler):
    """
       *注销页面处理*
    """
    def get(self):
        self.session.delete("username")
        self.redirect('/index/index.html')
class WechatLoginHandler(BaseHandler):
    #@tornado.web.asynchronous
    def webchat_redirect(self):
        self.redirect('/index/index.html')
    def get(self):
        uuid = itchat.get_QRuuid()
        while uuid is None:
            uuid = itchat.get_QRuuid()
        if itchat.get_QR(uuid):
            ret = itchat.get_QR(uuid)
        self.write(ret.getvalue())


