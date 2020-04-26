from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User, Group
from salt_restapi import models
from salt_restapi import forms
from salt_restapi.core import UploadFile
from django.contrib.auth.decorators import login_required


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
