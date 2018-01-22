#-*- coding:utf-8 -*-
'''程序入口'''
import tornado.web
import tornado.httpserver
from tornado.options import options,define
from settings import setting
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import handlers
define('port',8000,help="http port",type=int)
class Application(tornado.web.Application):
    def __init__(self):
        super(Application,self).__init__(handlers,**setting)

def run():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()