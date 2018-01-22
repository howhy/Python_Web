import datetime,json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import PBKDF2PasswordHasher,make_password
from utils.validation_code import gen_code
from django.core.cache import cache
from Artapiranti import  models
# Create your views here.
from django.views import View
from utils.uploadfile import  UploadFileThread,delUploadFile
class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url="/login/"
    def __init__(self):
        super(MyLoginRequiredMixin,self).__init__()

class Test(View):
    def get(self,request,*args,**kwargs):
         pass

class Admin(MyLoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        return render(request,"backend/index.html")

class Login(View):
    def get(self,request,*args,**kwargs):
         code, stream = gen_code()
         cache.set('validcode', code,timeout=120)
         return render(request, 'backend/login.html')

    def post(self,request,*args,**kwargs):
        login_err=""
        logincode=request.POST.get('validcode',None)
        redirecturl=request.POST.get('redirecturl')
        redirecturl=redirecturl.split('=')[-1] if 'next=' in redirecturl else '/admin/'
        if logincode.lower()==cache.get('validcode','').lower():
            user=authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
            if user:
                if user.is_active:
                    login(request,user)
                    request.session.set_expiry(3600)
                    return redirect(redirecturl)
                else:
                    login_err = "%s  is forbidden." % request.user.username
            else:
                login_err = "Username or Password error."
        else:
            login_err='Verification code error.'
        return render(request, 'backend/login.html', {'login_err':login_err})

class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('/login/')

class Validcode(View):
    """
    *验证码手动更新*
    """
    def get(self,request):
        code,stream=gen_code()
        cache.set('validcode', code)
        return HttpResponse(stream.getvalue())

class Product(MyLoginRequiredMixin,View):
    def get(self,request):
        product_objs=models.Product.objects.filter(state=1)
        return render(request, 'backend/product.html', {'productobjs': product_objs})

class Staff(MyLoginRequiredMixin,View):
    def get(self,request):
        data = request.GET
        action=data.get("action",None)
        if action=="del":
            id=data.get("id",None)
            models.Staff.objects.filter(id=id).update(state=0,update_time=datetime.datetime.now())
        staff_objs=models.Staff.objects.filter(state=1)
        return render(request, 'backend/staff.html', {'staffobjs': staff_objs})

    def post(self,request):
        data=request.POST
        photo = request.FILES.get("photo", "")
        nationalflag = request.FILES.get("nationalflag", "")
        uploadfileThread = UploadFileThread(filelist=[photo,nationalflag])
        uploadfileThread.start()
        #uploadfileThread.join()
        if uploadfileThread.flag:
            id = data.get('id', None)
            staff_dict = dict(
                username=data.get('username', None),
                position=data.get('position', None),
                age=data.get('age', None),
                nationality=data.get('nationality', None)
            )
            if photo:
                staff_dict["photo"] = photo.name
            if nationalflag:
                staff_dict["nationalFlag"] = nationalflag.name
            if id:
                staff_dict["update_time"] = datetime.datetime.now()
                models.Staff.objects.filter(id=id).update(**staff_dict)
            else:
                new_staff = models.Staff(**staff_dict)
                new_staff.save()
            return HttpResponse(json.dumps({"msg": "submit success", "result": "ok"}))
        return HttpResponse(json.dumps({"msg": str(uploadfileThread.msg), "result": "error"}))

class Blog(MyLoginRequiredMixin,View):
    def get(self,request):
        blog_objs=models.Blog.objects.filter(state=1)
        return render(request, 'backend/blog.html', {'blogobjs': blog_objs})

class Parter(MyLoginRequiredMixin,View):
    def get(self,request):
        data = request.GET
        action=data.get("action",None)
        if action=="del":
            id=data.get("id",None)
            models.Parter.objects.filter(id=id).update(state=0,update_time=datetime.datetime.now())
        parter_objs=models.Parter.objects.filter(state=1)
        return render(request, 'backend/parter.html', {'parterobjs': parter_objs,})

    def post(self,request):
        data=request.POST
        file = request.FILES.get("logo", "")
        uploadfileThread=UploadFileThread(filelist=[file])
        uploadfileThread.start()
        if uploadfileThread.flag:
            id = data.get('id', None)
            parter_dict = dict(
                name=data.get('name', None),
                website=data.get('website', None)
            )
            if file:
                parter_dict["logo"]=file.name
            if id:
                parter_dict["update_time"]=datetime.datetime.now()
                models.Parter.objects.filter(id=id).update(**parter_dict)
            else:
                new_parter =models.Parter(**parter_dict)
                new_parter.save()
            return HttpResponse(json.dumps({"msg": "submit success", "result": "ok"}))
        return HttpResponse(json.dumps({"msg": str(uploadfileThread.msg), "result": "error"}))

class ContactUs(MyLoginRequiredMixin,View):
    def get(self,request):
        data = request.GET
        action=data.get("action",None)
        if action=="del":
            id=data.get("id",None)
            del_contactus=models.ContactUs.objects.filter(id=id)
            delUploadFile(del_contactus[0].logo)
            del_contactus.update(state=0,update_time=datetime.datetime.now())
        contactus_objs=models.ContactUs.objects.filter(state=1)
        return render(request, 'backend/contactus.html', {'contactusobjs': contactus_objs})

    def post(self,request):
        data=request.POST
        file = request.FILES.get("logo", "")
        uploadfileThread=UploadFileThread(filelist=[file])
        uploadfileThread.start()
        #uploadfileThread.join()
        if uploadfileThread.flag:
            id = data.get('id', None)
            contactus_dict = dict(
                name=data.get('name', None),
                phone=data.get('phone', None),
                email=data.get('email', None),
                address=data.get('address', None))
            if file:
                contactus_dict["logo"] = file.name
            if id:
                contactus_dict["update_time"] = datetime.datetime.now()
                models.ContactUs.objects.filter(id=id).update(**contactus_dict)
            else:
                new_contactus = models.ContactUs(**contactus_dict)
                new_contactus.save()
            return HttpResponse(json.dumps({"msg": "submit success", "result": "ok"}))
        return HttpResponse(json.dumps({"msg": str(uploadfileThread.msg), "result": "error"}))

class Copyright(MyLoginRequiredMixin,View):
    def get(self,request):
        data = request.GET
        action=data.get("action",None)
        if action=="del":
            id=data.get("id",None)
            models.Copyright.objects.filter(id=id).update(state=0,update_time=datetime.datetime.now())
        copyright_objs=models.Copyright.objects.filter(state=1)
        return render(request, 'backend/copyright.html', {'copyrightobjs': copyright_objs})

    def post(self,request):
        data=request.POST
        id = data.get('id', None)
        copyright_dict = dict(
            content=data.get('content', None))
        if id:
            copyright_dict["update_time"]=datetime.datetime.now()
            models.Copyright.objects.filter(id=id).update(**copyright_dict)
        else:
            new_copyright =models.Copyright(**copyright_dict)
            new_copyright.save()
        return redirect('/copyright/')

class TimeLine(MyLoginRequiredMixin,View):
    def get(self,request):
        data = request.GET
        action=data.get("action",None)
        if action=="del":
            id=data.get("id",None)
            models.TimeLine.objects.filter(id=id).update(state=0,update_time=datetime.datetime.now())
        timeline_objs=models.TimeLine.objects.filter(state=1)
        return render(request, 'backend/timeline.html', {'timelineobjs': timeline_objs})

    def post(self,request):
        data=request.POST
        file = request.FILES.get("logo", "")
        uploadfileThread=UploadFileThread(filelist=[file])
        uploadfileThread.start()
        if uploadfileThread.flag:
            id = data.get('id', None)
            timeline_dict = dict(
                content=data.get('content', None),
            )
            if file:
                timeline_dict["img"]=file.name
            if id:
                timeline_dict["update_time"] = datetime.datetime.now()
                models.TimeLine.objects.filter(id=id).update(**timeline_dict)
            else:
                new_timeline = models.TimeLine(**timeline_dict)
                new_timeline.save()
            return HttpResponse(json.dumps({"msg": "submit success", "result": "ok"}))
        return HttpResponse(json.dumps({"msg": str(uploadfileThread.msg), "result": "error"}))

