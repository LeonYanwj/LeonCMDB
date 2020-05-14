from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User, Group
from saltapi import models
from saltapi import forms
from saltapi.core import UploadFile
from saltapi.core import SaltCtrl
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def batch_add(request):
    """
    文件接收 view
    :param request: 请求信息
    :return:
    """
    if request.method == "POST":
        f = request.FILES.get('file')
        f_obj = UploadFile(f)
        f_obj.save_sql()
        return HttpResponse("Upload file sccuess")
    else:
        return render(request,'agent_upload_file.html')

@login_required
def salt_environment(request):
    if request.method == "POST":
        obj = forms.SaltConfigEnv(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            models.SaltConfigEnv.objects.update_or_create(**obj.cleaned_data)
        else:
            print(obj.errors)
        return render(request,'saltConfig.html',{'obj':obj})
    else:
        obj = forms.SaltConfigEnv()
    return render(request,'saltConfig.html',{"obj":obj})


@login_required
def node_list(request):
    if request.method == "GET":
        obj = models.AgentDeployHostMess.objects.all()
        return render(request,'tables-footable.html',{"agent_host":obj})

def salt_agent_deploy(request):
    if request.method == "POST":
        handler = SaltCtrl(request)
        handler.data_is_valid()
        handler.deploy_agent()

    return HttpResponse("该接口只支持POST提交")