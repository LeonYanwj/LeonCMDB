from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asset(models.Model):
    """
    此表用于，创建相关资产
    1.asset_type_chioces:资产分类,设备信息，做项目前应统计好所有的硬件设备
        spareparts：备件
    2.management_ip：管理IP
    3.contract：合同
    4.trade_date：购买时间
    4.expre_date：过保时间
    business_unit：业务单元（部分机器可能处于空闲状态）
    tags:标签方便以后统计
    admin：管理员
    idc：所属IDC机房，关联机房
    status_choices：资产所处的集中状态
    memo：备注
    create_date：创建时间
    update_date：更新时间
    owndevice:所属的物理机
    zhizhaoshang<---->Manufactory  Alex源码是想把所有的硬件都有一个制造商，后来整合进了asset表中
    """

    asset_type_choices = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('storagedevice', u'存储设备'),
        ('securitydevice', u'安全设备'),
        ('idcdevice', u'机房设备'),
        ('accescories', u'备件'),
        # ('switch', u'交换机'),
        # ('router', u'路由器'),
        # ('firewall', u'防火墙'),
        # ('storage', u'存储设备'),
        # ('NLB', u'NetScaler'),
        # ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        # ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    name = models.CharField(max_length=64,unique=True)
    sn = models.CharField(u'资产编号',max_length=64,unique=True)
    management_ip = models.GenericIPAddressField(u'管理IP',blank=True,null=True)
    #zhizaoshang ----- Manufactory
    manufactory = models.ForeignKey('Manufactory',verbose_name=u'制造商',blank=True,null=True)
    contract = models.ForeignKey('Contract',verbose_name=u'合同',blank=True,null=True)
    trade_date = models.DateField(u'购买时间',null=True,blank=True)
    expire_date = models.DateField(u'过保时间',null=True,blank=True)
    price = models.FloatField(u'价格',null=True,blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True)
    tags = models.ManyToManyField('Tag',blank=True,null=True)
    admin = models.ForeignKey('UserAdmin',verbose_name=u'资产管理员',null=True,blank=True)
    cabinet = models.ForeignKey('Cabinet',verbose_name=u'IDC机柜',null=True,blank=True)
    owndevice = models.ForeignKey('Owndevice',verbose_name=u'所属物理机',null=True,blank=True)

    status_choices = (
        (0,'在线'),
        (1,'已下线'),
        (2,'未知'),
        (3,'故障'),
        (4,'备用'),
    )
    status = models.SmallIntegerField(choices=status_choices,default=0)
    memo = models.TextField(u'备注',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
    def __str__(self):
        return '<id:%s name:%s>'%(self.id,self.name)

class Server(models.Model):
    """
    服务器设备
    os_type:生产最好使用FK，因为方便后续统计系统类型
    """
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0,'PC服务器'),
        (1,'刀片机'),
        (2,'小型机')
    )
    created_by_choices = (
        ('auto','Auto'),
        ('manual','Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices,verbose_name=u'服务器类型',default=0)
    created_by = models.CharField(choices=created_by_choices,max_length=32,default='auto')

    #虚拟机自关联，此字段为保留字段
    #hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True)
    model = models.CharField(verbose_name=u'型号',max_length=128,null=True,blank=True)
    raid_type = models.CharField(u'raid类型',max_length=512,blank=True,null=True)
    os_type = models.CharField(u'操作系统类型',max_length=64,blank=True,null=True)
    os_distribution = models.CharField(u'发行版本',max_length=64,blank=True,null=True)
    os_release = models.CharField(u'操作系统版本',max_length=64,blank=True,null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'
    def __str__(self):
        return '%s sn:%s'%(self.asset.name,self.asset.sn)

class Owndevice(models.Model):
    """
    由于server表中有host
    """

    owndevice = models.CharField('主机',max_length=32,blank=True,null=True)
    memo = models.TextField('备注信息',max_length=128,blank=True,null=True)

    def __str__(self):
        return self.owndevice

    class Meta:
        verbose_name = '所属物理机'
        verbose_name_plural = '所属物理机'

class SafetyDevice(models.Model):
    """
    安全设备
    PS：SecurityDevice-->alex SafetyDevice-->Leon调用需要改变
    asset:与asset中的数据一一对应
    sub_asset：设备类型
    """

    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0,'防火墙'),
        (1,'入侵检测设备'),
        (2,'互联网网关'),
        (3,'运维审计系统'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices,verbose_name=u'服务器类型',default=0)
    def __str__(self):
        return self.asset.id

class NetworkDevice(models.Model):
    '''
    网络设备
    vlan_ip：VLAN的IP
    intranet_ip：内网IP
    model：型号
    fireware：固件
    port_num:端口个数
    device_detail：设备的详细信息
    。。。。
    '''

    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0,'路由器'),
        (1,'交换机'),
        (2,'负载均衡'),
        (3,'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices,verbose_name=u'网络设备类型',default=0)
    vlan_ip = models.GenericIPAddressField(u'vlanip',blank=True,null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP',blank=True,null=True)
    model = models.CharField(u'型号',max_length=128,blank=True,null=True)
    fireware = models.ForeignKey('Software',blank=True,null=True)
    port_num =models.SmallIntegerField(u'端口个数',blank=True,null=True)
    device_detail = models.TextField(u'设备信息信息',blank=True,null=True)
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)

class Software(models.Model):
    """
    软件资产asset关联资产表
    软件资产因为与上面的资产总表做了一一对应，所以注释os，
    """
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0,'OS'),
        (1,'办公\开发软件'),
        (2,'业务软件'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices,verbose_name=u'软件资产分类',default=0)
    license_num = models.IntegerField(verbose_name="授权数")
    # os_distribution_choices = (('windows','Windows'),
    #                            ('centos','CentOS'),
    #                            ('ubuntu', 'Ubuntu'))
    # type = models.CharField(u'系统类型', choices=os_types_choice, max_length=64,help_text=u'eg. GNU/Linux',default=1)
    # distribution = models.CharField(u'发型版本', choices=os_distribution_choices,max_length=32,default='windows')
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)

    # language_choices = (('cn',u'中文'),
    #                     ('en',u'英文'))
    # language = models.CharField(u'系统语言',choices = language_choices, default='cn',max_length=32)
    # #version = models.CharField(u'版本号', max_length=64,help_text=u'2.6.32-431.3.1.el6.x86_64' )

    def __str__(self):
        return self.version
    class Meta:
        verbose_name = '软件系统'
        verbose_name_plural = '软件系统'

class CPU(models.Model):
    """
    cpu组件
    cpu_model:cpu的型号
    cpu_count：服务器物理个数
    cpu_core_count:n核n线程

    """
    asset = models.ForeignKey('Asset')
    cpu_model = models.CharField(u'型号',max_length=128,blank=True)
    cpu_count = models.SmallIntegerField(u'物理CPU个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    class Meta:
        verbose_name = 'cpu组件'
        verbose_name_plural = 'cpu组件'

    def __str__(self):
        return self.cpu_model

class RAM(models.Model):
    """
    内存组件

    """
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号',max_length=128,blank=True,null=True)
    model = models.CharField(u'内存型号',max_length=128)
    slot = models.CharField(u'插槽',max_length=64)
    capacity = models.IntegerField(u'内存大小（MB）')
    memo =models.CharField(u'备注',max_length=128,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)
    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")
    auto_create_field = ['sn','slot','model','capacity']

class Disk(models.Model):
    """
    磁盘信息表
    """
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号',max_length=128,blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号',max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    # disk_iface_chioce = (
    #     ('SATA','SATA'),
    #     ('SAS','SAS'),
    #     ('SCSI','SCSI'),
    #     ('SSD','SSD'),
    #     ('virtual','virtual'),
    # )
    iface_type = models.CharField(verbose_name=u'接口类型',max_length=64,null=True,blank=True)
    memo = models.TextField(u'备注',blank=True,null=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    auto_craete_fields = ['sn','slot','manufactory','model','capacity']
    class Meta:
        unique_together = ("asset","slot")
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'
    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)

class NIC(models.Model):
    """
    网卡组件
    name：名字
    model：型号
    bonding：绑定
    memo：备注
    create_date：创建时间
    update_date：更新时间
    词表和上面的表一样绑定了asset
    """
    asset = models.ForeignKey("Asset")
    name = models.CharField(u'网卡名字',max_length=64,blank=True,null=True)
    sn = models.CharField(u'SN号',max_length=128,blank=True,null=True)
    model = models.CharField(u'网卡类型',max_length=16)
    macaddress = models.CharField(u'MAC',max_length=64,unique=True)
    ipaddress = models.GenericIPAddressField('IP',blank=True,null=True)
    netmask = models.CharField(max_length=64,blank=True,null=True)
    bonding = models.CharField(max_length=64,blank=True,null=True)
    memo = models.TextField(u'备注',max_length=128,null=True,blank=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u'网卡'

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']

class RaidAdaptor(models.Model):
    """
    raid卡相关信息
    目前只有Dell服务器相关的收集raid信息的工具
    词表也和asset资产表进行一一关联
    """
    asset = models.OneToOneField("Asset")
    #sn列注释的原因，因为个人觉得raid无sn号，所以不关联
    # sn = models.CharField(u'SN号',max_length=128,blank=True,null=True)
    slot = models.CharField(u'插槽',max_length=64)
    model = models.CharField(u'类型',max_length=64,blank=True,null=True)
    memo = models.TextField(u'备注',blank=True,null=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('asset','slot')

class Manufactory(models.Model):
    """
    制造商
    """
    manufactory = models.CharField(u'品牌名称',max_length=64,unique=True)
    support_num = models.CharField(u'支持电话',max_length=32,blank=True,null=True)
    memo = models.TextField(u'备注',max_length=128,blank=True,null=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = '品牌'

class BusinessUnit(models.Model):
    """
    业务线
    """
    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField(u'业务线', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class Contract(models.Model):
    """
    合同表
    sn：这里是指的合同标号
    memo：备注
    price：合同金额
    detail：合同详情
    """
    sn = models.CharField(u'合同号',max_length=128,unique=True)
    name = models.CharField(u'合同名称',max_length=64)
    mem0 = models.TextField(u'备注',blank=True,null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同明细',blank=True,null=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    #license_num为明白是什么啥意思
    license_num = models.IntegerField(u'license数量',blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'

    def __str__(self):
        return self.name

class Cabinet(models.Model):
    """
    idc机房表

    """
    idc = models.ForeignKey("IDC")
    number = models.CharField(max_length=32)


    def __str__(self):
        return self.number

    class Meta:
        unique_together = ('idc','number')

class IDC(models.Model):
    """
    机房
    """
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"

class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey('UserAdmin')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class EventLog(models.Model):
    """事件"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Asset')
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey('UserAdmin', verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'

class ReqLog(models.Model):
    asset = models.ForeignKey(Asset)
    level_message_chioce = (
        ('error','error'),
        ('info','info'),
        ('warning', 'warning')
    )
    level_message = models.CharField(choices=level_message_chioce,verbose_name=u'错误等级',max_length=16)
    message = models.TextField(verbose_name=r'详细信息',null=True,blank=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'

    def __str__(self):
        return "资产id: %s 日志等级: %s"%(self.asset.id,self.level_message)

class UserAdmin(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    department = models.CharField(max_length=32,null=True,blank=True)
    phone = models.IntegerField()

class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

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
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
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
    approved_by = models.ForeignKey('UserAdmin', verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    token = models.CharField(max_length=32,null=True,blank=True)
    phone = models.IntegerField()

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"
