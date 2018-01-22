#-coding:utf-8-*-
import datetime
import models
from uuid import uuid4
import os
import re
import requests
from Blog.common.dbhandler import DBHandler

url = "https://www.zhsir.org/category3"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}

def get_content(suburl):
    req = requests.get(suburl, headers=header, timeout=60)
    subhtm = req.content.decode('utf-8').replace('\r\n','')
    reg = '<article class="post_body">(.*?)</article>'
    content = re.findall(reg, subhtm)
    return content

def get_html(url):
    req = requests.get(url, headers=header, timeout=60)
    htm = req.content.decode('utf-8').replace('>\r\n','>')
    reg='<h2 class="post_title"><a href="(.+?)">(.+?)</a></h2>.+?<section class="post_body">(.+?)</section>'
    alist = re.findall(reg, htm)
    return alist


def save_db():
    for suburl,title,brief in get_html(url):
        content = get_content(suburl)
        art = models.Article(id=str(uuid4()), title=title, brief=brief, content=content, category_id=1, image='')
        DBHandler(art).add()
if __name__=='__main__':
    save_db()
