from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Newstu(models.Model):
    rollno = models.IntegerField()
    name = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    stu_class = models.IntegerField()
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stuinfo' 

class Bookdts(models.Model):
    bid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)    
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-bid',)

    class Meta:
        db_table = 'bkinfo' 

class issbktb(models.Model):
    bid = models.CharField(max_length=50)
    sid = models.CharField(max_length=50)  
    bkname = models.CharField(max_length=50)   
    issbkdt = models.DateField(auto_now_add=True)
    retdt = models.DateField(null=True)
    fine = models.IntegerField(null=True)
       
    def __str__(self):
        return self.bid

    class Meta:
        db_table = 'issbkinfo' 

