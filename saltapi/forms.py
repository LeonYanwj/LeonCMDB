from django.forms import forms
from django.forms import fields

class FileUploadForm(forms.Form):
    agentMessFile = forms.FileField()

class SaltConfigEnv(forms.Form):
    webserver = fields.GenericIPAddressField(
        required=True,
        error_messages={"required":"主机地址不能为空","invaild":"提交的必须要是IPV4或者是IPV6地址"}
    )
    timeout = fields.IntegerField(
        required=True,
        error_messages={"requied": "超时时间不能为空","invaild": "提交必须要数字"}
    )
    salt_master = fields.GenericIPAddressField(
        error_messages={"required": "salt-master地址不能为空","invaild": "提交的必须要ipv4或是ipv6地址"}
    )