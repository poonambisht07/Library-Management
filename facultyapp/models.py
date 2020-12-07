from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

# Create your models here.
class Bookdts(models.Model):
    bid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)    
    author = models.CharField(max_length=50)
    cat = models.CharField(max_length=50)
   
    def __str__(self):
        return self.title
            
    class Meta:
        ordering = ('-bid',)

    class Meta:
        db_table = 'bkinfo' 

def get_expiry():
    return datetime.today()+timedelta(days=15)
class issbktb(models.Model):
    s_enroll = models.CharField(max_length=50)
    s_name = models.CharField(max_length=50)
    b_name = models.CharField(max_length=50)
    b_id = models.CharField(max_length=50)
    issbkdt = models.DateField(auto_now_add=True)
    expirydt = models.DateField(default=get_expiry)
    fine = models.IntegerField(null=True,blank=True)
       
    def __str__(self):
        return self.s_enroll

    class Meta:
        db_table = 'issbkinfo' 

class register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnt = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to="profiles/%Y/%m/%d",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)    
    gender = models.CharField(max_length=250,default="Male")
    enrollment = models.CharField(max_length=40, null=True,blank=True)
    branch = models.CharField(max_length=40, null=True,blank=True)  
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

class contact_us(models.Model):
    name = models.CharField(max_length=250)
    cnt = models.IntegerField(blank=True, unique= True)
    sub = models.CharField(max_length=250)
    msg = models.TextField()
    added_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"    

    