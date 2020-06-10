# Register your models here.
from django.contrib import admin
from asset import models
from asset import core


class AssetApprovalAdmin(admin.ModelAdmin):
    '''
    list_display:django admin表中显示的字段
    list_filter:按照指定字段进行过滤
    search_fields:按照指定的字段进行搜索
    list_editable:在admin中修改字段值
    actions:调用指定函数方法，处理admin中的数据
    '''
    list_display = ('sn','asset_type','internal_ipaddr','approved')

    list_filter = ('asset_type','os_type')
    search_fields = ('sn','os_type')
    list_editable = ('asset_type','approved')

    actions = ['asset_approval',]
    def asset_approval(self,request,querysets):
        #action默认给三个参数，request就是request，querysets就是models obj
        print("--------asset approval.....",self,request,querysets)
        for obj in querysets:
            asset_handler = core.Asset(request)
            if asset_handler.data_is_valid_without_id(obj):
                obj.approved = True
                obj.save()
                print(asset_handler.response)

    asset_approval.short_description = "新资产审批"



admin.site.register(models.NewAssetApprovalZone,AssetApprovalAdmin)
admin.site.register(models.Server)
admin.site.register(models.UserAdmin)