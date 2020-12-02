from django.shortcuts import render, get_object_or_404, reverse
from django.shortcuts import redirect
from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from datetime import datetime,date
import json
from django.core.mail import EmailMessage

# Create your views here.
def mainpage(request):
    context = {}
    if "user_id" in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User, id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/dashboard")
    
    res = contact_us.objects.all().order_by("-id")[:5]
    context = {'rec':res}

    return render(request,'library/base.html', context)

def signup(request):
    if request.method == "POST":
        n = request.POST.get('tbname')
        e = request.POST.get('tbemail')
        p = request.POST.get('tbpassword')
        p = make_password(p)
        ct = request.POST.get('tbcontact')
        r = request.POST.get('tbroll')
        en= request.POST.get('tbenr')
        branch = request.POST.get('tbranch')
        # print(en,branch)
        try:
            rec = User.objects.create(first_name=n.title(),email=e,password=p,username=e)
            
            if r == "teacher":
                rec.is_staff = True
                rec.save()

                rec1 = register(user=rec,cnt=ct,enrollment=en,branch=branch.title())            
                rec1.save()
            
            return render(request, 'library/signup.html', {'msg':'Mr/Miss. {} Thanks for register'.format(n)})
        except:
            return render(request, 'library/signup.html', {'msg':'Try again'})
    else:
        return render(request,'library/signup.html')

def user_check(request):
    if request.method == "GET":
        un = request.GET.get('username')
        check = User.objects.filter(username=un)
        # print(check)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def enr_check(request):
    if request.method == "GET":
        enr = request.GET.get('enroll')
        check = register.objects.filter(enrollment=enr)
        print(check)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def contactus(request):
    context = {}
    if request.method == "POST":
        n = request.POST.get("tbname")
        cnt = request.POST.get("tbcnt")
        sub = request.POST.get("tbsub")
        msg = request.POST.get("tbmsg")

        # print(n, cnt, sub, msg)
        rec = contact_us.objects.create(
            name=n, cnt=cnt,sub=sub,msg=msg
        )
        rec.save()
        msg = "Dear {}, Thanks for your Feedback.".format(n)
        context ={'msg': msg}
        
    return render(request,'library/contactus.html', context)

def aboutus(request):
    
    return render(request,'library/aboutus.html')

def profile(request):
    context = {}
    check = register.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register.objects.get(user__id=request.user.id)
        # print(data)
        context["data"] = data
    return render(request,'library/profile.html', context)

def user_login(request):
    if (request.method == 'POST'):
        e = request.POST.get('tbemail')
        p = request.POST.get('tbpassword')
        # print(request.POST)         
        user = authenticate(request, username=e, password=p)    
        if user:            
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect('/admin')
            else:
                res = HttpResponseRedirect("/dashboard")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    # print(user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
                
        else:
            return render(request, 'library/login.html', {'result':'User Id and Password is Invalid'})

    return render(request,'library/login.html')
     
def forget_pass(request):
    context = {}
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get("npass")

        # user = get_object_or_404(User, username=un)
        user = User.objects.get(username = un)
        user.set_password = pwd
        user.save()
        context = {'status':"Password Change Successfully"}

    return render(request,'library/forget_pass.html', context)

import random
def reset_pass(request):
        un = request.GET.get("username")
        
        try:
            user = get_object_or_404(User, username=un)
            otp = random.randint(1000,9999)
            msg = "Dear, {} \n{} is your One Time Password (OTP) \n Don't Share it with others.".format(user.username, otp)
            try:
                email = EmailMessage("Account Verfication", msg, to =[user.email])
                email.send()
                return JsonResponse({"status":"sent", "email":user.email, "rotp":otp})            
            except:
                return JsonResponse({"status":"error","email":user.email})
        except:
                return JsonResponse({"status":"failed"})

        

def user_logout(request):
    logout(request)
    res = HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res

def edit_profile(request):
    context = {}
    check = register.objects.filter(user__id=request.user.id)
    # print("c: ", check)
    if len(check)>0:
        data = register.objects.get(user__id=request.user.id)
        context["data"] = data
    if (request.method == 'POST'):
        
        s_n = request.POST.get('tbname')
        s_age = request.POST.get('tbage')
        s_city = request.POST.get('tbcity')
        s_gender = request.POST.get('tbgender')
        s_cnt = request.POST.get('tbcnt')
        
        usr = User.objects.get(id=request.user.id)
        usr.first_name = s_n        
        usr.save()

        data.cnt = s_cnt
        data.age = s_age
        data.city = s_city
        data.gender = s_gender
        data.save()

        if "tbimg" in request.FILES:
            img = request.FILES["tbimg"]
            data.profile_pic = img
            data.save()
        context["msg"] = "Changes Saved Successfully"
        
    return render(request,'library/editprofile.html', context)

def change_pass(request):
    context = {}
    check = register.objects.filter(user__id=request.user.id)
    
    if len(check) > 0:
        data = register.objects.get(user__id=request.user.id)
        # print(data)
        context["data"] = data
    if request.method == "POST":
        cp = request.POST.get("cpwd")
        np = request.POST.get("npwd")

        usr = User.objects.get(id=request.user.id)
        un = usr.username
        cpd = usr.check_password(cp)
        if cpd == True:
            usr.set_password(np)
            usr.save()
            context['msg'] = "Password Change Succesfully"
            context['col'] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context['msg'] = "Incorrect Current Password"
            context['col'] = "alert-danger"
    print(context)
    return render(request,'library/changepass.html',context)

# @login_required
def addstudent(request): 
        context = dict()  
        newst = User.objects.all().exclude(is_staff=1).order_by('-id')
       
        page = request.GET.get('page')
        paginator = Paginator(newst,5)

        try:
            user = paginator.page(page)
        except PageNotAnInteger:
            user = paginator.page(1)
        except EmptyPage:
            user = paginator.page(paginator.num_pages)

        context = {'users': user}
        return render(request, "library/addstudent.html", context)

# @login_required
def viewstu(request):
    stu = register.objects.filter(user__id=request.user.id)
    for i in stu:
        print(i.enrollment)
    rec = issbktb.objects.filter(s_enroll=i.enrollment)

    context = {'info' : rec }
    return render(request, "library/showstu.html",context)


# @login_required
def books(request):
    context = {}
    if request.method == 'POST':       
        b_id = request.POST.get('id')
        b_title = request.POST.get('title')
        b_author = request.POST.get('author')
        b_cat = request.POST.get('category')
                
        bdt = Bookdts.objects.create(
            bid = b_id,            
            title = b_title.title(),
            author = b_author.title(),
            cat = b_cat.title(),                        
            )       
        bdt.save()
        context = {'msg':'Your Record Saved Successfully'}        
    return render(request, "library/book.html", context)

# @login_required
def bksearch(request):         

    return render(request, "library/bsearch.html")


# # @login_required
def bsrch(request):   
        if(request.method == 'POST'):            
            title = request.POST["in_name"]   
            # print(title)         
            brec = Bookdts.objects.filter(title__icontains = title)           
            record = list()
            if (brec.exists()):            
                for rec in brec:
                    b_info = dict()
                    b_info['bid']= rec.bid
                    b_info['title']= rec.title                   
                    b_info['author']= rec.author
                    b_info['cat']= rec.cat
                    record.append(b_info)                            
            return HttpResponse(json.dumps(record))


# @login_required
def showbk(request):
    
    context = dict()  
    try:  
        res=Bookdts.objects.all().order_by('bid')
        
    except Books.DoesNotExist :
        print("record not found")          

    page = request.GET.get('page')
    # print(page)
    paginator = Paginator(res, 5)
    # print(paginator)
    try:
        bk = paginator.page(page)
        # print(user)
    except PageNotAnInteger:
        bk = paginator.page(1)
        # print(user)
    except EmptyPage:
        bk = paginator.page(paginator.num_pages)
        # print(user) 
    context ={'info' : bk}   
    return render(request, "library/showbk.html", context)


# @login_required
def edit_bk_view(request):
    if(request.method=='POST'):
        sid=request.POST.get('tbId')
        bid = request.POST.get('bkid')
        title = request.POST.get('bktitle')
        author = request.POST.get('bkauthor')
        cat = request.POST.get('category')
              
        try:
            rec = Bookdts.objects.get(id=sid)
            rec.bid=bid
            rec.title=title.title()
            rec.author=author.title()
            rec.cat=cat.title()          
            rec.save()
            return redirect('/showbk/')
        except Exception as ex:
            print(ex)
    else:

     sid=request.GET.get('id')
     records=Bookdts.objects.get(id=sid)
     context={'data':records}
     return render(request,'library/editbook.html',context)


# @login_required
def del_bk_view(request):

    id=request.GET.get('id')
    Bookdts.objects.filter(id=id).delete()
    return redirect('/showbk')

def stu_check(request):
    context = dict()
    bk = Bookdts.objects.all()
    print(bk)
    st = User.objects.all().exclude(is_staff=1).order_by("first_name")
    context = {'bk':bk,'st':st}
    return render(request, "library/addissbk.html", context)

def get_issbk(request):
    context = dict()
    bk = Bookdts.objects.all()
    # print(bk)
    sd = {}
    for i in User.objects.all().exclude(is_staff=1):
        sd[i]={}
        sd[i]["name"]=i.first_name.title()
        sd[i]["enr"] = i.register.enrollment
    # print(sd)
      
    return JsonResponse({"booklist":list(bk.values()),"stulist":list(sd.values())})
   
import re
# @login_required
def issbk(request):
    context = dict()
    if(request.method == 'POST'): 
        s = request.POST.get('stlist')
        # print(s)
        regex = re.compile(r'(\d+)')
        k = regex.split(str(s))
        # print(k)
        bn = request.POST.get('bklist')
        # print(bn)
        reg = re.compile(r'(\d+)')
        b = (reg.split(str(bn)))
        # print(b)
        issbk = issbktb.objects.create(           
            s_name = k[0],            
            s_enroll = k[1],
            b_name = b[0],
            b_id = b[1]                               
            )                   
        issbk.save()
        context = {'msg':'Book Issued Succesfully'}        
    return render(request, "library/addissbk.html", context)


# @login_required
def delete_stu_view(request):
    id=request.GET.get('id')
    Newstu.objects.filter(id=id).delete()
    return redirect('/showstu')

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
@login_required
def showissbkdt(request):        
    rec = issbktb.objects.all().order_by('-id')
    for i in rec:
        iss = i.issbkdt
        d = (date.today()-iss).days
        fine=0
        if d > 15:
            day=d-15
            fine=day*10
        # print(fine)
        r = issbktb.objects.filter(id=i.id)
        for j in r:
            j.fine=fine
            j.save()
   
    page = request.GET.get('page')
    # print(page)
    paginator = Paginator(rec, 5)
    # print(paginator)
    try:
        user = paginator.page(page)
        print(user)
    except PageNotAnInteger:
        user = paginator.page(1)
        print(user)
    except EmptyPage:
        user = paginator.page(paginator.num_pages)
        print(user)
    context = {'users':user}
    return render(request, "library/showissbkdt.html", context)

def send_mail(request):
    context = {}
    ch = register.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register.objects.get(user__id=request.user.id)
        context['data'] = data

    if request.method == "POST":

        rec = request.POST.get("to").split(",")
        sub = request.POST.get("sub")
        msg = request.POST.get("msg")
                
        try:
            em = EmailMessage(sub,msg,to=rec)   
            em.send()
            context["status"] = "Email Sent"
            context["cls"] = "alert-success"
        except:
            context['status'] = 'Sorry, Mail could not send'
            context['cls'] = 'alert-danger'
    # print(context)
    return render(request, 'library/sendmail.html', context)

   