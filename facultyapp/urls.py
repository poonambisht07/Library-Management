"""EMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [

    path('about/',aboutus, name='about_page'),
    path('contact/',contactus, name='contact_page'),
    path('dashboard/',profile, name='dashboard'),
    path('',mainpage, name='main_view'),
    path('login/',user_login, name='login_view'),
    path('forget_pass/', forget_pass, name='forget_pass'),
    path('reset_pass/', reset_pass, name="reset_pass"),
    path('signup/',signup, name='signup_view'),  
    path('user_check/',user_check, name='user_check'),
    path('user_logout/', user_logout, name='user_logout'),  
    path('editprofile/', edit_profile, name='edit_profile'),   
    path('change_pass/', change_pass, name='change_pass'),   
    path('send_mail/', send_mail, name='send_mail'),
    path('addstudent/',addstudent),   
    path('viewstu/',viewstu, name='viewstu'),
    path('stu_check/', stu_check, name='stu_check'),  
    path('addbooks/',books),
    path('bsearch/',bksearch, name='bsearch'),
    path('booksrch/',bsrch),
    path('showbk/',showbk),    
    path('addissbk/',issbk),    
    path('get_issbk/',get_issbk),
    path('delstu/', delete_stu_view, name='delstu'),
    path('editbk/', edit_bk_view, name='editbk'), 
    path('delbk/', del_bk_view, name='delbk'),
    path('showissbkdt/', showissbkdt),
    path('enr_check/',enr_check, name='enr_check'), 
    
]   

