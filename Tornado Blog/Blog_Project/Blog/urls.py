#-*- coding:utf-8 -*-
from webblog_app.handler import IndexHandler,ShowDetailHandler,CommentHandler,MainHandler,SelfBlogHandler,BackendHandler,BackendEditHandler,ShowLognoteHandler
from Blog.user.userhandler import  LoginHandler,LogoutHandler,EnrollHandler,WechatLoginHandler
from common.basehandler import CheckCodeHandler,QRCodeHandler,UploadFileHandler,DownloadFileHandler

handlers = [
    (r'/', MainHandler),
    (r'/enroll', EnrollHandler),
    (r'/login', LoginHandler),
    (r'/wechat_login/', WechatLoginHandler),
    (r'/logout', LogoutHandler),
    (r'/checkcode/', CheckCodeHandler),
    (r'/qrcode/', QRCodeHandler),
    (r'^/index/([\w-]+).html$', IndexHandler),
    (r'^/backend/([\w-]+).html$', BackendHandler),
    (r'^/backendedit/([\w-]+).html$', BackendEditHandler),
    (r'/(?P<blogname>\w+)/(?P<lid>\d+).html$',ShowLognoteHandler),
    (r'/(?P<blogname>[\w-]+).html$',SelfBlogHandler),
    (r'/(?P<blogname>[\w-]+)/(?P<aid>[\w-]+).html$',ShowDetailHandler),
    (r'/comment', CommentHandler),
    (r'/uploadfile', UploadFileHandler),
    (r'/downloadfile', DownloadFileHandler),
]
