from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

class AgentDeployHostMess(models.Model):
    """agent批量安装主机信息"""
    hostip = models.CharField("主机ip",max_length=64,blank=True)
    os_type = models.CharField("系统类型",max_length=64,blank=True)
    remote_port = models.IntegerField("远程登录端口",blank=True)
    remote_user = models.CharField("远程登录用户",max_length=64,blank=True)
    remote_password = models.CharField("远程登录密码",max_length=64,blank=True)
    craete_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    text =  models.TextField(blank=True)

    class Meta:
        unique_together = ("id","hostip")
        verbose_name = "agent安装表"
        verbose_name_plural = "agent安装表"

    def __str__(self):
        return "<id:%s host:%s>"%(self.id,self.hostip)

class SaltConfigEnv(models.Model):
    """salt env"""
    webserver = models.GenericIPAddressField()
    timeout = models.IntegerField()
    salt_master = models.GenericIPAddressField()