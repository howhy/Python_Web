#-coding:utf-8-*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
import sys
from uuid import uuid4
import os
import re
import requests
from bs4 import BeautifulSoup
from Blog.main import Application
import models
from Blog.common.dbhandler import DBHandler

url="http://www.51cto.com/"
header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
def get_html(url):
    req=requests.get(url,headers=header,timeout=60)
    htm=req.content.decode('gbk')
    article=r'<div class="pic"><a href=(.+?) target=.+?><img src=(.+?)></a><p><a href=.+? target=.+?>(.+?)</a></p></div>'
    article_reg=re.compile(article)
    ret=re.findall(article_reg,htm)
    return ret
def save_article():
    ret=get_html(url)
    for art in ret:
        try:
            imgname = str(uuid4())
            con = requests.get(art[0], headers=header, timeout=10)
            bs = BeautifulSoup(con.content.decode('gbk'), "html.parser")
            title=bs.h2.string
            brief=bs.select('.wznr p')
            kind=art[2]
            txt = bs.select('.zwnr p')
            content=""
            for text in txt:
                content += str(text) if text else ""
            img_urls=bs.select('.zwnr img',limit=1)
            for imgurl in img_urls:
                image = requests.get(imgurl['src'], headers=header, timeout=60)
                today_str = datetime.date.today().strftime("%Y%m%d")
                img_path = "%s/%s/" % (Application().settings.get('static_path')+'/images/', today_str)
                if not os.path.isdir(img_path):
                    os.makedirs(img_path)
                imgpath = img_path + imgname + '.jpg'
                with open(imgpath, 'wb') as f:
                    f.write(image.content)
            if content and type and title and brief:
                art= models.Article(id=str(uuid4()),category_id=1, title=title,brief=str(brief[0]), content=content.replace("51CTO.com", '').replace("51CTO", ''), image='images/%s/%s.jpg'%(today_str,imgname))
                DBHandler(art).add()
        except requests.exceptions.ConnectionError:
            print 'download error'
            continue
if __name__=='__main__':
    save_article()
