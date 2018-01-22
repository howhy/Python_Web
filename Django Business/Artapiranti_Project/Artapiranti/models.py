from django.db import models

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=128)
    img=models.CharField(max_length=64)
    description=models.TextField()
    platform=models.CharField(max_length=256)
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class Parter(models.Model):
    name=models.CharField(max_length=64)
    website=models.URLField()
    logo=models.CharField(max_length=32)
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class ContactUs(models.Model):
    name=models.CharField(max_length=64,null=False)
    logo=models.CharField(max_length=32,null=False)
    email=models.CharField(max_length=64,null=False)
    phone=models.CharField(max_length=32,null=False)
    address=models.CharField(max_length=128,null=False)
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class Staff(models.Model):
    username=models.CharField(max_length=32)
    position=models.CharField(max_length=32)
    age=models.IntegerField()
    photo=models.CharField(max_length=32)
    nationality=models.CharField(max_length=32)
    nationalFlag=models.CharField(max_length=32)
    selfIntroduction=models.TextField()
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class Copyright(models.Model):
    content=models.CharField(max_length=256)
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class TimeLine(models.Model):
    img=models.CharField(max_length=32)
    content=models.CharField(max_length=64)
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    staff = models.ForeignKey(Staff, to_field='id', on_delete=models.CASCADE, )
    title=models.CharField(max_length=128)
    content=models.TextField()
    state=models.SmallIntegerField(default=1)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)








