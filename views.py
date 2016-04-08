from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lapp.models import profile,application
import json
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from django.core.mail import send_mail

@csrf_exempt
def loginme(request):
	usr=request.POST.get('username')
	pwd=request.POST.get('password')
	user=authenticate(username=usr,password=pwd)
	if user is not None:
		print user,"yo"
		login(request,user)
		return redirect("/home/")
	else:
		return redirect("/")

@csrf_exempt
def index(request):
	return render(request,'index2.html')

@csrf_exempt
def home(request):
	if request.user.is_staff: #hod
		myinfo=profile.objects.filter(user=User.objects.get(id=request.user.id))
		apps=application.objects.filter(branch=myinfo[0].branch,status=0)
		context={
			'myinfo' : myinfo,
			'applications' : apps,
			}
		return render(request,"home_hod.html",context)
	else: # for faculty
		print User.objects.get(id=request.user.id),"cool"
		myinfo=profile.objects.filter(user=User.objects.get(id=request.user.id))
		myapps=application.objects.filter(user=request.user)
		context={
			'myinfo' : myinfo,
			'myapps' : myapps,
			}
		return render(request,"home_fc.html",context)

@csrf_exempt
@login_required(login_url="/")
def apply(request):
	datefrom=str(request.POST['datefrom'])
	why=request.POST['why']
	prox=request.POST['prox']
	#leave_type=int(request.POST['type'])
	leave_type=0
	myprofile=profile.objects.get(user=request.user)
	myprofile.leaves_left-=1
	myprofile.save()
	myhod=profile.objects.get(branch=myprofile.branch,user=User.objects.filter(is_staff=True))
	#print myhod.user.username
	send_mail('Leave application', 'Respected Sir i have requested for a leave kindly visit the site for the details url:-http://127.0.0.1:8000/', 'pictleave@gmail.com',
    [myhod.user.email], fail_silently=False)
	application.objects.create(user=request.user,status=0,reason=why,proxy=prox,datefrom=datefrom,dateto=datefrom,branch=myprofile.branch,type_leave=leave_type)
	return render(request,'subm.html')

@csrf_exempt
@login_required(login_url="/")
def upd(request):
	return render(request,'updt.html')


@login_required(login_url="/")
def accept(request,aid):
	app1=application.objects.get(id=aid)
	app1.status=1
	app1.save()
	send_mail('Leave application', 'Respected Sir Youre leave application status has been updated kindly visit the site url:-http://127.0.0.1:8000/', 'pictleave@gmail.com',[app1.user.email], fail_silently=False)
	return redirect("/home")

@login_required(login_url="/")
def decline(request,aid):
	app1=application.objects.get(id=aid)
	app1.status=2
	app1.save()
	send_mail('Leave application', 'Respected Sir Youre leave application status has been updated kindly visit the site', 'pictleave@gmail.com',[app1.user.email], fail_silently=False)
	pro=profile.objects.get(user=app1.user)
	pro.leaves_left+=1
	pro.save()
	return redirect("/home")


def mylogout(request):
	logout(request)
	return redirect("/")
