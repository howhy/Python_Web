#_*_coding:utf-8_*_
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import math, string
import hashlib,time
from io import BytesIO
import os
import qrcode
from Blog.settings import setting

#字体的位置，不同版本的系统会有不同
font_path = '%s/fonts/msyh.ttf'%setting['static_path']
#font_path = '/Library/Fonts/Hanzipen.ttc'
#生成几位数的验证码
number = 4
#生成验证码图片的高度和宽度
size = (100,40)
#背景颜色，默认为白色
bgcolor = (255,255,255)
#字体颜色，默认为蓝色
fontcolor = (0,255,127)
#干扰线颜色。默认为红色
linecolor = (255,0,0)
#是否要加入干扰线
draw_line = True
#加入干扰线条数的上下限
line_number = (1,5)
def hash_key():
    hs=hashlib.sha1()
    hs.update(str(time.time()).replace('.',''))
    return hs.hexdigest()[:10]
def gen_text():
    source = list(string.ascii_letters)
    for index in range(0,10):
        source.append(str(index))
    return ''.join(random.sample(source,number))#number是生成验证码的位数

#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = linecolor)

def gene_code():
    width,height = size #宽和高
    image = Image.new('RGBA',(width,height),bgcolor) #创建图片

    font = ImageFont.truetype(font_path,32) #验证码的字体和字体大小
    #font = ImageFont.truetype(25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image) #创建画笔
    #text = "我是中国人" #生成字符串
    text = gen_text() #生成字符串
    #print(text)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,\
        font= font,fill=fontcolor) #填充字符串

    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
   
    image = image.transform((width + 20, height +10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    streamimg=BytesIO()
    image.save(streamimg,'PNG')
    return text,streamimg

def gen_qrcode(string, logo=""):
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库
    :param string: 二维码字符串
    :param path: 生成的二维码保存路径
    :param logo: logo文件路径
    :return:
    """
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=1
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    icon = Image.open(logo)
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
    imgqrcode= BytesIO()#gen_qrcode("http://139.199.212.60/", "qr.png", "head2.jpg")
    img.save(imgqrcode, 'PNG')
    return imgqrcode

if __name__ == "__main__":
    gene_code() 

