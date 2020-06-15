from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from asset import core
from asset import plugins
from django.contrib import auth
import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from asset import models
# Create your views here.

@csrf_exempt
def asset_with_no_asset_id(request):

    if request.method == "POST":
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()

        return HttpResponse(json.dumps(res))


@csrf_exempt
def asset_report(requests):
    if requests.method == "POST":
        ass_hander = core.Asset(requests)
        if ass_hander.data_is_valid():
            ass_hander.data_inject()

        return HttpResponse(json.dumps(ass_hander.response))

@login_required
def index(requests):
    hosts_obj = models.Asset.objects.all()
    return render(requests,'index.html',locals())

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login.html/')

def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            print("登录通过认证，将登录信息记录到session中，并跳转")
            try:
                auth.login(request, user)
                request.session.set_expiry(60 * 30)
                print("跳转的目的",request.POST.get('next'))
                return HttpResponseRedirect(request.POST.get("next") if request.POST.get("next") != "None" or request.POST.get("next") != "/" else "/index.html/")

            except Exception:
                    return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})

        else:
            return render(request,'login.html',{'name':username,'pwd':password})
    else:
        next_url = request.GET.get("next")
        return render(request, 'login.html',{"next_url":next_url})

@login_required
def root(request):
    return HttpResponseRedirect('/login.html/')

@login_required
def test(request):
    return render(request,'serverlist.html')