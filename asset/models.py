from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AppSystem(models.Model):
    """
    fk1: 所有者可能会和用户表进行关联
    fk2: 发布的流水线可能会和流水线表进行关联
    fk3: 开发团队可能会和团队表进行关联
    """
    system = models.ForeignKey('System',verbose_name='所属系统')
    supportteam = models.ManyToManyField('SupportTeam',verbose_name="执行信息",blank=True)
    name = models.CharField(verbose_name="应用系统名称",max_length=200,blank=True,null=True)
    enName = models.CharField("英文简称",max_length=200,blank=True,null=True)
    description = models.CharField("描述",max_length=200,blank=True,null=True)
    state = models.CharField('状态',max_length=50,null=True,blank=True)
    department = models.CharField('组织部门',max_length=50,null=True,blank=True)
    secuityLev = models.IntegerField('等保等级',null=True,blank=True)
    businessTy = models.CharField('业务类型',max_length=50,null=True,blank=True)
    releasePipeline = models.CharField('发布流水线',max_length=50,null=True,blank=True)
    updateDate = models.DateTimeField(auto_now=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True,blank=True)

    class Meta():
        verbose_name = "应用系统"
        verbose_name_plural = "应用系统"

    def __str__(self):
        return "%s %s"%(self.name,self.state)


class Center(models.Model):

    name = models.CharField('中心名称',max_length=200,null=True,blank=True)
    enName = models.CharField('英文简称',max_length=200,null=True,blank=True)
    description = models.CharField('描述',max_length=200,null=True,blank=True)

    class Meta():
        verbose_name = "中心"
        verbose_name_plural = "中心"

    def __str__(self):
        return self.name

class Environment(models.Model):

    name = models.CharField('环境名称',max_length=200,null=True,blank=True)
    enName = models.CharField('英文名称',max_length=200,null=True,blank=True)
    description = models.CharField('描述',max_length=200,null=True,blank=True)

    class Meta():
        verbose_name = "环境"
        verbose_name_plural = "环境"

    def __str__(self):
        return self.name

class ChildSystem(models.Model):

    name = models.CharField('子系统名称',max_length=50,null=True,blank=True)
    enName = models.CharField('英文名称',max_length=200,null=True,blank=True)
    description = models.CharField('描述',max_length=200,null=True,blank=True)
    state_choices = (
        (0,'已上线'),
        (1,'已下线'),
        (2,'故障'),
        (3,'维修中'),
    )
    state = models.CharField('状态',max_length=50,choices=state_choices,blank=True,default=0)
    businessLevel = models.CharField('业务级别',max_length=50,null=True,blank=True)
    applicationPort = models.IntegerField('端口',null=True,blank=True)
    secondSupportTeam = models.CharField('二线支持团队',max_length=50,null=True,blank=True)
    ownerMainName = models.CharField('所有者',max_length=50,null=True,blank=True)
    ownerPrePareName = models.CharField('所有者备',max_length=50,blank=True,null=True)
    createDate = models.DateTimeField('创建时间',auto_now_add=True)
    updateDate = models.DateTimeField('修改时间',auto_now=True)

    class Meta():
        verbose_name = '子系统'
        verbose_name_plural = '子系统'

    def __str__(self):
        return "<%s:%s>"%(self.name,self.state)

class Cluster(models.Model):
    name = models.CharField('集群名称',max_length=200,null=True,blank=True)
    env = models.CharField("集群环境",max_length=200,null=True,blank=True)
    architecture = models.CharField('模块架构',max_length=50,null=True,blank=True)
    deploymentType = models.CharField("模块类型",max_length=50,null=True,blank=True)
    state_choices = (
        (0,'运行中'),
        (1,'已下线'),
        (2,'集群异常'),
        (3,'维护中')
    )
    state = models.CharField("状态",max_length=50,choices=state_choices,blank=True,default=0)
    class Meta():
        verbose_name = "集群信息"
        verbose_name_plural = "集群信息"

    def __str__(self):
        return "%s--> %s"%(self.name,self.state)


class ModelName(models.Model):
    name = models.CharField("模块名称",max_length=50,blank=True,null=True)
    env = models.CharField("所处环境",max_length=50,blank=True,null=True)


class Server(models.Model):
    """x86 服务器表"""
    name = models.CharField("物理机名称",max_length=200,blank=True)
    serviceIp = models.CharField('服务ip',max_length=64,blank=True,null=True)

class System(models.Model):
    """虚拟机，真实的业务系统"""
    server = models.ForeignKey('Server',verbose_name='所属物理机',blank=True)
    name = models.CharField("物理机名称",max_length=200,blank=True)
    serviceIp = models.CharField('服务ip',max_length=64,blank=True,null=True)

class SupportTeam(models.Model):
    """支持团队"""
    name = models.CharField("名称",max_length=200,blank=True,null=True)

class NewAssetApprovalZone(models.Model):
    """新资产待添加到主机列表中"""
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices,max_length=64,blank=True,null=True)
    ipaddr = models.CharField("服务器ip地址",max_length=64,blank=True,null=True)