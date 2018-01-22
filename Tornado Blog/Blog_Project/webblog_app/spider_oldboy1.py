#-coding:utf-8-*-
import datetime
import models
from uuid import uuid4
import os
import re
import requests
from Blog.common.dbhandler import DBHandler
from bs4 import BeautifulSoup

url = "https://www.abcdocker.com/abcdocker/category/tomcat/"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}

def get_content(suburl):
    req = requests.get(suburl, headers=header, timeout=60)
    subhtm = req.content.decode('utf-8')
    bs = BeautifulSoup(subhtm, "html.parser")
    content=bs.find('article')
    return content

def get_html(url):
    req = requests.get(url, headers=header, timeout=60)
    htm = req.content.decode('utf-8').replace('>\r\n','>')
    reg='<a href="(.+?)"><img width="280" height="210" src="(.+?)" class="attachment-content size-content wp-post-image" alt="(.+?)" srcset='
    alist = re.findall(reg, htm)
    alist=re.findall(reg,htm)
    return alist


def save_db():
    for suburl,imgsrc,title in get_html(url):
        imgname=str(uuid4())
        # image = requests.get(imgsrc, headers=header, timeout=60)
        # imgpath = imgname + '.jpg'
        # with open(imgpath, 'wb') as f:
        #     f.write(image.content)
        content = get_content(suburl)
        art = models.Article(id=imgname, title=title, brief=title, content=str(content), category_id=1, image='images/%s'%imgname,user_id='73653f80-000e-48f1-90e4-91e22e13d229')
        DBHandler(art).add()
        #break
if __name__=='__main__':
    save_db()
    #print get_html(url)
    #print get_content('https://www.abcdocker.com/abcdocker/2526')
