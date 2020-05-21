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
    path('dashboard/',home_view),
    path('',index, name='login_view'),
    path('signup/',signup, name='signup_view'),    
    path('addstudent/',addstudent),   
    path('showstu/',showstu),
    path('search/',search),   
    path('addbooks/',books),
    path('bsearch/',bksearch, name='bsearch'),
    path('booksrch/',bsrch),
    path('showbk/',showbk),    
    path('addissbk/',issbk),
    path('delstu/', delete_stu_view, name='delstu'),
    path('editstudent/', edit_stu_view, name='editstu'), 
    path('editbk/', edit_bk_view, name='editbk'), 
    path('delbk/', del_bk_view, name='delbk'),
    path('showissbkdt/', showissbkdt),
    path('adreturn/',addreturndt, name='adreturn'), 
    path('editissbk/',edit_issbk_view, name='editissbk'),
    path('deleteissbk/',delete_issbk_view, name='deleteissbk'),
]   

