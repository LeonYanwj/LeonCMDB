from django.db import models
from django.contrib.auth.models import User
from common.models import UUIDTools

# Create your models here.

class AppSystem(models.Model):
    """
    fk1: 所有者可能会和用户表进行关联
    fk2: 发布的流水线可能会和流水线表进行关联
    fk3: 开发团队可能会和团队表进行关联
    """
    id = models.CharField(max_length=32, primary_key=True, default=UUIDTools.uuid1_hex, editable=False, db_column='id')
    supportteam = models.ManyToManyField('SupportTeam',verbose_name="维护团队",blank=True,db_column='support_team')
    name = models.CharField(verbose_name="应用系统名称",max_length=200,blank=True,null=True,db_column='name')
    enName = models.CharField("英文简称",max_length=200,blank=True,null=True,db_column='en_name')
    description = models.CharField("描述",max_length=200,blank=True,null=True,db_column='description')
    state = models.CharField('状态',max_length=50,null=True,blank=True,db_column='state')
    department = models.CharField('组织部门',max_length=50,null=True,blank=True,db_column='department')
    businessTy = models.CharField('业务类型',max_length=50,null=True,blank=True,db_column='business_type')
    releasePipeline = models.CharField('发布流水线',max_length=50,null=True,blank=True,db_column='release_pipeline')
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
        db_table = "center"
        verbose_name = "中心"
        verbose_name_plural = "中心"

    def __str__(self):
        return self.name

class Environment(models.Model):

    name = models.CharField('环境名称',max_length=200,null=True,blank=True)
    enName = models.CharField('英文名称',max_length=200,null=True,blank=True)
    description = models.CharField('描述',max_length=200,null=True,blank=True)

    class Meta():
        db_table = "environment"
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
        db_table = 'child_System'
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
        db_table = 'cluster'
        verbose_name = "集群信息"
        verbose_name_plural = "集群信息"

    def __str__(self):
        return "%s--> %s"%(self.name,self.state)

class ServerInformation(models.Model):
    """x86 服务器基本信息获取"""
    id = models.CharField(primary_key=True,max_length=32,default=UUIDTools.uuid1_hex, editable=False, db_column='id')
    systemId = models.CharField(max_length=32,blank=True,null=True,verbose_name='所属应用系统',db_column='system_id')
    name = models.CharField("物理机名称",max_length=200,blank=True,db_column='name')
    serviceIp = models.CharField('服务ip',max_length=64,blank=True,db_column='service_ip')
    serviceMac = models.CharField("服务ip Mac地址",max_length=64,blank=True,db_column='service_mac')
    manageip = models.CharField("管理ip",max_length=64,blank=True,null=True,db_column='manage_ip')
    manageMac = models.CharField("管理地址Mac",max_length=64,blank=True,null=True,db_column='manage_mac')
    os_type = models.CharField("操作系统类型",max_length=64,blank=True,null=True,db_column='os_type')
    os_name = models.CharField("操作系统名称",max_length=64,blank=True,null=True,db_column='os_name')
    os_version = models.CharField("操作系统版本",max_length=16,blank=True,null=True,db_column='os_version')
    os_bits = models.CharField("操作系统位数",max_length=16,blank=True,null=True,db_column='os_bits')
    cpu_logic_count = models.SmallIntegerField("CPU逻辑核心数",blank=True,null=True,db_column='cpu_logic_count')
    cpu_model = models.CharField("cpu型号",max_length=64,blank=True,null=True,db_column='cpu_model')
    cpu_frequency = models.CharField("cpu频率",max_length=16,blank=True,null=True,db_column='cpu_frequency')
    mem_size = models.CharField("内存大小",max_length=16,blank=True,null=True,db_column='mem_size')
    mem_frequency = models.CharField("内存频率",max_length=16,blank=True,null=True,db_column='mem_frequency')
    disk_size = models.CharField("硬盘大小",max_length=16,blank=True,null=True,db_column='disk_size')
    description = models.CharField("描述",max_length=248,blank=True,null=True,db_column='description')
    zone = models.CharField("区域",max_length=64,blank=True,null=True,db_column='zone')
    room = models.CharField("所在机房",max_length=64,blank=True,null=True,db_column='room')
    owner = models.CharField("设备维护人",max_length=64,blank=True,null=True,db_column='owner')
    state = models.CharField("状态",max_length=16,blank=True,null=True,db_column='state')
    sn = models.CharField("设备sn",max_length=64,blank=True,null=True,db_column='sn')
    create_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    class Meta:
        db_table = 'server_information'
        verbose_name = "服务器"
        verbose_name_plural = "服务器"

    def __str__(self):
        return self.name

class Servermonitor(models.Model):
    """服务器实时信息收集"""
    serverId = models.CharField(max_length=32,blank=True,null=True,verbose_name='所属应用系统',db_column='server_id')
    cpu_usage = models.FloatField("处理器使用率",max_length=32,blank=True)
    mem_usage = models.FloatField("内存使用率",max_length=32,blank=True)
    disk_usage = models.FloatField("硬盘使用率",max_length=32,blank=True)
    create_data = models.DateTimeField(auto_now=True,blank=True)

    class Meta:
        db_table = 'server_monitor'
        verbose_name = "服务器实时信息收集"
        verbose_name_plural = "服务器实时信息收集"

class SupportTeam(models.Model):
    """支持团队"""
    name = models.CharField("名称",max_length=200,blank=True,null=True)

class UserAdmin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    department = models.CharField(max_length=32,null=True,blank=True)
    phone = models.IntegerField()

class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""
    internal_ipaddr = models.CharField("内网ip地址",max_length=64,null=True,blank=True)
    external_ipaddr = models.CharField("外部ip地址",max_length=64,null=True,blank=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
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
    asset_type = models.CharField(choices=asset_type_choices, max_length=64,default='server',blank=True, null=True)
    manufactory = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey('UserAdmin', verbose_name=u'批准人', blank=True, null=True,on_delete=models.CASCADE)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"

class EventLog(models.Model):
    """事件表"""
    text = models.TextField(verbose_name="记录",null=True,blank=True)