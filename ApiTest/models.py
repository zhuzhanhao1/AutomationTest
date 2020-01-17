from django.db import models

# Create your models here.
# python3 manage.py migrate Api --fake

'''
blank=True
默认值为blank=Flase，表示默认不允许为空，
blank=True admin级别可以为空
 
null=True
默认值为null=Flase，表示默认不允许为空
null=True 数据库级别可以为空
'''
class SingleApi(models.Model):
    """
    单一接口
    """
    caseid = models.AutoField(primary_key=True,max_length=200,unique=True)
    casename = models.CharField(max_length=100,verbose_name="用例名称")
    identity = models.CharField(max_length=50,verbose_name="用户身份")
    url = models.CharField(max_length=250,verbose_name="访问路径")
    method = models.CharField(max_length = 20,verbose_name="请求方式")
    header = models.CharField(max_length=200,verbose_name="请求头",null=True,blank=True)
    params = models.TextField(verbose_name="请求参数",null=True,blank=True)
    body = models.TextField(verbose_name="请求体内容",null=True,blank=True)
    exceptres = models.TextField(verbose_name="期望结果",null=True,blank=True)
    result = models.TextField(verbose_name="执行结果",null=True,blank=True)
    belong = models.CharField(max_length=50,verbose_name="所属模块")
    system = models.CharField(max_length=50, verbose_name="所属系统")
    sortid = models.IntegerField(verbose_name="排序号",blank=True,null=True)
    duration = models.FloatField(verbose_name="响应时长",blank=True,null=True)
    head = models.CharField(max_length=200, verbose_name="负责人",null=True)

    def __str__(self):
        return self.casename

    class Meta:
        verbose_name = '单一接口'
        verbose_name_plural = '单一接口管理'

class LeftMenu(models.Model):
    """
    左侧一级菜单
    """
    id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=150, verbose_name="区域")

    title = models.CharField(max_length=150, verbose_name="标题")

    icon =  models.CharField(max_length=150, verbose_name="图标",default="&#xe674")
    href = models.CharField(max_length=150, verbose_name="链接")
    spread = models.BooleanField(default=False, verbose_name="默认不展开")
    children = models.TextField(verbose_name="子菜单",default=[])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '左侧菜单'
        verbose_name_plural = '左侧菜单管理'


class ChildMenu(models.Model):
    """
    二级菜单
    """
    id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=150, verbose_name="区域")

    classification = models.ForeignKey(LeftMenu, on_delete=models.CASCADE, verbose_name='所属分类')

    title = models.CharField(max_length=150, verbose_name="标题")
    nav = models.CharField(max_length=150,verbose_name="左侧导航的键",null=True,blank=True)
    icon =  models.CharField(max_length=150, verbose_name="图标",default="&#xe674")
    href = models.CharField(max_length=150, verbose_name="链接")
    spread = models.BooleanField(default=False, verbose_name="默认不展开")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '二级菜单'
        verbose_name_plural = '二级菜单管理'


class SystemRole(models.Model):
    """
    系统角色
    """
    id = models.AutoField(primary_key=True)
    identity = models.CharField(max_length=100,verbose_name="角色英文名")
    role = models.CharField(max_length=150, verbose_name="角色")
    username = models.CharField(max_length=250, verbose_name="用户名")
    password = models.CharField(max_length=250, verbose_name="密码")
    system = models.CharField(max_length=150, verbose_name="所属系统")
    token = models.CharField(max_length=250, verbose_name="令牌信息",null=True,blank=True)
    ip = models.CharField(max_length=200,verbose_name="IP地址",null=True,blank=True)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = '系统角色'
        verbose_name_plural = '系统角色管理'


class Link(models.Model):
    """
    友情链接
    """
    id = models.AutoField(primary_key=True)
    logo = models.CharField(max_length=250, verbose_name="网站logo")
    websites = models.CharField(max_length=250,verbose_name="网站名称")
    url = models.CharField(max_length=250, verbose_name="网址")

    def __str__(self):
        return self.websites

    class Meta:
        verbose_name_plural = '友情链接'


class Testurl(models.Model):
    """
    测试网址
    """
    id = models.AutoField(primary_key=True)
    logo = models.CharField(max_length=250, verbose_name="网站logo")
    websites = models.CharField(max_length=250,verbose_name="网站名称")
    url = models.CharField(max_length=250, verbose_name="网址")
    apidocument = models.CharField(max_length=250, verbose_name="接口文档")

    def __str__(self):
        return self.websites

    class Meta:
        verbose_name_plural = '测试网址'


# class SystemLog(models.Model):
#     """
#     项目动态
#     """
#     id = models.AutoField(primary_key=True)
#     time = models.DateTimeField(max_length=128, verbose_name='操作时间')
#     type = models.CharField(max_length=50, verbose_name='操作类型')
#     operationObject = models.CharField(max_length=50, verbose_name='操作对象')
#     user = models.CharField(max_length=50,verbose_name='操作人')
#     description = models.CharField(max_length=1024, blank=True, null=True,  verbose_name='描述')
#
#     def __unicode__(self):
#         return self.type
#
#     class Meta:
#         verbose_name = '操作日志'
#         verbose_name_plural = '操作日志'


#流程API接口测试
class ProcessApi(models.Model):
    caseid = models.AutoField(primary_key=True,unique=True)
    casename = models.CharField(max_length=100,verbose_name="用例名称")
    identity = models.CharField(max_length=50,verbose_name="用户身份")
    url = models.CharField(max_length=550,verbose_name="访问路径")
    method = models.CharField(max_length = 20,verbose_name="请求方式")
    header = models.CharField(max_length=200,verbose_name="请求头",null=True,blank=True)
    params = models.TextField(verbose_name="请求参数",null=True,blank=True)
    body = models.TextField(verbose_name="请求体内容",null=True,blank=True)
    exceptres = models.CharField(max_length=250,verbose_name="期望结果",null=True,blank=True)
    result = models.TextField(verbose_name="执行结果",null=True,blank=True)
    belong = models.CharField(max_length=200,verbose_name="所属模块")
    # belong = models.ForeignKey(ChildMenu, on_delete=models.SET_NULL, verbose_name='所属模块',related_name="childmenu_processapi",null=True)
    isprocess = models.CharField(max_length=20,verbose_name="是否有依赖",default=False)
    depend_id = models.CharField(max_length=20,verbose_name="依赖的caseID",null=True,blank=True)
    depend_key = models.CharField(max_length=500,verbose_name="依赖的key",null=True,blank=True)
    replace_key = models.CharField(max_length=500,verbose_name="替换的key",null=True,blank=True)
    replace_position = models.CharField(max_length=50,verbose_name="替换的内容区域", null=True,blank=True)
    sortid = models.IntegerField(verbose_name="排序号",default=1)
    system = models.CharField(max_length=50, verbose_name="所属系统")
    duration = models.FloatField(verbose_name="响应时长",null=True,blank=True)
    head = models.CharField(max_length=200, verbose_name="负责人",null=True,blank=True)

    def __str__(self):
        return self.casename

    class Meta:
        verbose_name_plural = '接口流程管理'



class LocustApi(models.Model):
    """
    接口性能测试
    """
    caseid = models.AutoField(primary_key=True,max_length=200,unique=True)
    identity = models.CharField(max_length=50,verbose_name="用户身份")
    url = models.CharField(max_length=250,verbose_name="访问路径")
    method = models.CharField(max_length = 20,verbose_name="请求方式")
    header = models.CharField(max_length=200,verbose_name="请求头",null=True,blank=True)
    params = models.TextField(verbose_name="请求参数",null=True,blank=True)
    body = models.TextField(verbose_name="请求体内容",null=True,blank=True)
    ip = models.CharField(max_length = 100,verbose_name="ip地址")

    class Meta:
        verbose_name = '接口性能测试'
        verbose_name_plural = '接口性能测试'
