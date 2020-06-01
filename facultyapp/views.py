from django.shortcuts import render, redirect
from django.http import request, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
import json


# Create your views here.
@login_required
def home_view(request):

    return render(request,'faculty/home.html')

def index(request):
    if (request.method == 'POST'):
        e = request.POST.get('tbemail')
        p = request.POST.get('tbpassword')
                 
        user = authenticate(request, username=e, password=p)    
        if user:            
            login(request, user)
            return HttpResponseRedirect('dashboard')
        else:
            return render(request, 'faculty/login.html', {'result':'User Id and Password is Invalid'})

    return render(request,'faculty/login.html')
    
def signup(request):
    if (request.method == 'POST'):
        n = request.POST.get('tbname')
        e = request.POST.get('tbemail')
        p = request.POST.get('tbpassword')
        p = make_password(p)
        
        try:
            rec = User.objects.create(first_name=n,email=e,password=p,username=e)
            rec.save()
            return render(request, 'faculty/signup.html', {'msg':'Thanks for register'})

        except:
            return render(request, 'faculty/signup.html', {'msg':'try again'})
    else:
        return render(request,'faculty/signup.html')


@login_required
def addstudent(request): 
    context = dict()  
    if(request.method == 'POST'):
        stu_roll = request.POST['rollno']
        stu_name = request.POST['name']
        stu_fname = request.POST['fname']
        stu_email = request.POST['email']
        stu_class = request.POST['class']
        
        newst = Newstu.objects.create(
            rollno = stu_roll,
            name = stu_name,
            fname = stu_fname,
            email = stu_email,
            stu_class = stu_class,            
            )
        newst.save()
        context = {'msg' : 'Your record saved'}
    return render(request, "faculty/addstudent.html", context)

@login_required
def showstu(request):
        
    if(request.method == 'POST'):
        clss = request.POST.get('srh')
        print(clss)

        rec = Newstu.objects.filter(stu_class=clss)
        context = {'info' : rec }

    else:
        
        rec = Newstu.objects.all().order_by('stu_class')
        context = {'info' : rec }
    return render(request, "faculty/showstu.html", context)

@login_required
def search(request):
    context = dict()
    if(request.method == 'POST'):
        clss = request.POST.get('cls')
        rollno = request.POST.get('rollno')
        print(clss)
        print(rollno)
        rec = Newstu.objects.filter(Q(stu_class=clss) & Q(rollno=rollno))
        for r in rec:
            print(r.rollno)
        context = {'info' : rec }

    return render(request, "faculty/search.html", context)


@login_required
def books(request):
    if(request.method == 'POST'):
        b_id = request.POST.get('id')
        b_title = request.POST.get('title')
        b_author = request.POST.get('author')
        b_price = request.POST.get('price')
        
        bdt = Bookdts.objects.create(
            bid = b_id,            
            title = b_title,
            author = b_author,
            price = b_price,                        
            )       
        bdt.save()        
    return render(request, "faculty/book.html")

@login_required
def bksearch(request):         

    return render(request, "faculty/bsearch.html")


@login_required
def bsrch(request):   
        if(request.method == 'POST'):
            
            title = request.POST["in_name"]            
            brec = Bookdts.objects.filter(title__icontains = title)           
            record = list()
            if (brec.exists()):            
                for rec in brec:
                    b_info = dict()
                    b_info['bid']= rec.bid
                    b_info['title']= rec.title                   
                    b_info['author']= rec.author
                    b_info['price']= rec.price
                    record.append(b_info)                            
            return HttpResponse(json.dumps(record))


@login_required
def showbk(request):
    
    context = dict()  
    try:  
        res=Bookdts.objects.all().order_by('bid')
        context ={'info' : res}
    except   Books.DoesNotExist :
        print("record not found")          
        
    return render(request, "faculty/showbk.html", context)


@login_required
def edit_bk_view(request):
    if(request.method=='POST'):
        sid=request.POST.get('tbId')
        bid = request.POST.get('bkid')
        title = request.POST.get('bktitle')
        author = request.POST.get('bkauthor')
        price = request.POST.get('bkprice')
              
        try:
            rec = Bookdts.objects.get(id=sid)
            rec.bid=bid
            rec.title=title
            rec.author=author
            rec.price=price          
            rec.save()
            return redirect('/showbk/')
        except Exception as ex:
            print(ex)
    else:

     sid=request.GET.get('id')
     records=Bookdts.objects.get(id=sid)
     context={'data':records}
     return render(request,'faculty/editbook.html',context)


@login_required
def del_bk_view(request):

    id=request.GET.get('id')
    Bookdts.objects.filter(id=id).delete()
    return redirect('/showbk')


@login_required
def issbk(request):
    if(request.method == 'POST'):
        b_id = request.POST.get('bid')
        s_id = request.POST.get('sid')
        bk_name = request.POST.get('bkname')
        iss_dt = request.POST.get('issdt')        
        
        issbk = issbktb.objects.create(
            bid = b_id,            
            sid = s_id,
            bkname = bk_name,
            issbkdt = iss_dt,                                    
            )       
        issbk.save()        
    return render(request, "faculty/addissbk.html")


@login_required
def delete_stu_view(request):
    id=request.GET.get('id')
    Newstu.objects.filter(id=id).delete()
    return redirect('/showstu')


@login_required
def edit_stu_view(request):
    if(request.method=='POST'):
        sid=request.POST.get('tbId')
        r_no = request.POST.get('rollno')
        name = request.POST.get('name')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        s_class = request.POST.get('class')
        print("ffffffffffffffffffffff---", name)
        try:
            rec = Newstu.objects.get(id=sid)
            rec.rollno=r_no
            rec.name=name
            rec.fname=fname
            rec.email=email
            rec.stu_class=s_class
            rec.save()
            return redirect('/showstu/')
        except Exception as ex:
            print(ex)
    else:

     sid=request.GET.get('id')
     records=Newstu.objects.get(id=sid)
     context={'data':records}
     return render(request,'faculty/editstudent.html',context)


@login_required
def showissbkdt(request):
        
        rec = issbktb.objects.all()        
        context = {'info' : rec }
        return render(request, "faculty/showissbkdt.html", context)


@login_required
def addreturndt(request):
    if(request.method == 'POST'):
        s_id = request.POST.get('sid')
        ret_dt = request.POST.get('retdt')       
        r = issbktb.objects.get(sid=s_id)
        id = r.id
        r.retdt = ret_dt 
        r.save()

        rec = issbktb.objects.filter(id=id)  
        for r in rec:
            print(r.id)
            a = r.retdt
            b = r.issbkdt
            c = (a-b)
            print(c)
            c1 = (c.days)
            print(c1)
            if c1 > 1 :
                c1 += 1
                d = c1 * 5
                
            elif c1 == 1:
                d = c1 * 5               
            r.fine = d   
            r.save()         

    return render(request,"faculty/addretbk.html")

@login_required
def edit_issbk_view(request):
    if(request.method=='POST'):
        bk_id=request.POST.get('tbId')
        bid = request.POST.get('bid')
        bname = request.POST.get('name')
        sid = request.POST.get('sid')
        issdt = request.POST.get('issdt')
        retdt = request.POST.get('retdt')
        
        print("ffffffffffffffffffffff---", bname)
        try:
            rec = issbktb.objects.get(id=bk_id)
            rec.bid=bid
            rec.bkname=bname
            rec.sid=sid
            rec.issbkdt=issdt
            rec.retdt=retdt            
            rec.save() 

            rec = issbktb.objects.filter(id=bk_id)  
            for r in rec:
                print(r.id)
                a = r.retdt
                b = r.issbkdt
                c = (a-b)
                print(c)
                c1 = (c.days)
                print(c1)
                if c1 > 1 :
                    c1 += 1
                    d = c1 * 5
                    
                elif c1 == 1:
                    d = c1 * 5               
                r.fine = d   
                r.save()            
            return redirect('/showissbkdt/')
        except Exception as ex:
            print(ex)
    else:

     sid=request.GET.get('id')
     records=issbktb.objects.get(id=sid)
     context={'data':records}
     return render(request,'faculty/editissbk.html',context)

@login_required
def delete_issbk_view(request):
    id=request.GET.get('id')

    issbktb.objects.filter(id=id).delete()

    return redirect('/showissbkdt')

