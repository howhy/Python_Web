# -*- coding: utf-8 -*-
import os,sys
import threading
import traceback
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class UploadFileThread(threading.Thread):
    def __init__(self,filelist=None,*args):
        super(UploadFileThread,self).__init__()
        self.filelist=filelist
        self.args=args
        self.flag=True
        self.msg=""
    def run(self):
        try:
            for file in self.filelist:
                if file:
                    filename = file.name
                    file_path = os.path.join(root_dir, "static", "upload", filename)
                    if not os.path.exists(file_path):
                        with open(file_path, "wb+") as f:
                            for chunk in file.chunks():
                                f.write(chunk)
                    else:
                        raise FileExistsError("file has already exist.")
        except Exception as e:
            self.flag = False
            self.msg=e
            traceback.format_exception(sys.exc_info())


def delUploadFile(filename):
    file_path = os.path.join(root_dir, "static", "upload", filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)




