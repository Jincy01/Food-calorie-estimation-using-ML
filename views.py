from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
import datetime

from .models import *
import os
from yolov5 import detect

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=registerr(name=name,email=email,password=password)
        reg.save()
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif registerr.objects.filter(email=email,password=password).exists():
        userdetails=registerr.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
        
        return render(request,'index.html')
        
    else:
        return render(request, 'login.html', {'success':'Invalid email id or Password'})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)

def v_users(request):
    user = registerr.objects.all()
    return render(request, 'viewusers.html', {'result': user})

def test(request):
    return render(request,'test.html')

def addfile(request):
    if request.method=="POST":
        u_id = request.session['uid']
        
        file = request.FILES['file']
        try:
            os.remove("media/input/test.jpg")
        except:
            pass
        fs = FileSystemStorage(location="media/input")
        fs.save("test.jpg",file)
        fs = FileSystemStorage()
        fs.save(file.name,file)
        calorie=detect.run()

        cus=uploads(u_id=u_id,result=calorie,file=file)
        cus.save()
        return render(request,'result.html',{'res':calorie})
    return render(request,'test.html')
    
def v_result(request):
    uid=request.session['uid']
    user = uploads.objects.filter(u_id=uid)
    return render(request, 'viewresult.html', {'result': user})

def live(request):
    return render(request,'live.html')




def diet(request):
    return render(request,'adddieat.html')



def adddiet(request):
    if request.method=="POST":
        age_limit=request.POST.get('age_limit')
        con_calorie=request.POST.get('con_calorie')
       
        reg=diet_tbl(age_limit=age_limit,con_calorie=con_calorie)
        reg.save()
    return render(request,'index.html')



def view_diet(request):
    user = diet_tbl.objects.all()
    return render(request, 'viewdie.html', {'result': user})
