from rest_framework import serializers
from .models import SingleApi, LeftMenu, ChildMenu, SystemRole, \
    Link, Testurl, ProcessApi, LocustApi, SingleApiChild, FunctionCase, FunctionCaseChild

###########################SingleApi####################################

class SingleApiSerializers(serializers.ModelSerializer):
    '''
        单一接口
    '''
    class Meta:
        model = SingleApi
        fields = ('caseid', 'casename', 'identity', 'url','method','header','params','body',
                  'exceptres','result','belong','system','sortid','duration','head')  # 需要序列化的属性

class SingleApiResponseSerializers(serializers.ModelSerializer):
    '''
        单一接口，更新响应内容和响应延迟
    '''
    class Meta:
        model = SingleApi
        fields = ('result','duration')  # 需要序列化的属性

class SingleApiParamsSerializers(serializers.ModelSerializer):
    '''
        单一接口，更新请求中的Query参数
    '''
    class Meta:
        model = SingleApi
        fields = ('params',)  # 需要序列化的属性

class SingleApiBodySerializers(serializers.ModelSerializer):
    '''
        单一接口，更新请求中的Body参数
    '''
    class Meta:
        model = SingleApi
        fields = ('body',)  # 需要序列化的属性

class SingleApiHeadSerializers(serializers.ModelSerializer):
    '''
        单一接口，更新负责人参数
    '''
    class Meta:
        model = SingleApi
        fields = ('head',)  # 需要序列化的属性

class SingleApiIdentitySerializers(serializers.ModelSerializer):
    '''
        单一接口，更新负责人参数
    '''
    class Meta:
        model = SingleApi
        fields = ('identity',)  # 需要序列化的属性

###########################LeftMenu#########################################

class LeftMenuSerializers(serializers.ModelSerializer):
    '''
        头部菜单左侧一级菜单
    '''
    class Meta:
        model = LeftMenu
        depth = 1
        fields = ('title','icon','href','spread')


###########################ChildMenu#########################################

class ChildMenuSerializers(serializers.ModelSerializer):
    '''
        二级菜单
    '''
    class Meta:
        model = ChildMenu

        fields = ('title','icon','href','spread')

class ChildMenusSerializers(serializers.ModelSerializer):
    '''
        菜单管理列表
    '''
    class Meta:
        model = ChildMenu
        fields = ("id","nav",'title','icon','href','spread',"classification","area")

class GetParamsSer(serializers.ModelSerializer):
    '''
        belong参数
    '''
    class Meta:
        model = ChildMenu
        fields = ('title',"nav")

###########################SystemRole####################################

class SystemRoleSerializers(serializers.ModelSerializer):
    '''
        系统角色
    '''
    class Meta:
        model = SystemRole
        fields = ('id','role','username','password','token','system','ip')

class TokenSerializers(serializers.ModelSerializer):
    '''
        更新令牌信息/ip地址
    '''
    class Meta:
        model = SystemRole
        fields = ('token',)

class RoleSerializers(serializers.ModelSerializer):
    '''
        角色对应身份
    '''
    class Meta:
        model = SystemRole
        fields = ('role',)

###########################Link####################################

class LinkSerializers(serializers.ModelSerializer):
    '''
        友情链接
    '''
    class Meta:
        model = Link
        fields = ('id', 'logo','websites','url')

###########################Testurl####################################

class TesturlSerializers(serializers.ModelSerializer):
    '''
        测试网址
    '''
    class Meta:
        model = Testurl
        fields = ('id', 'logo','websites','url','apidocument')

###########################ProcessApi####################################

class ProcessApiListSerializers(serializers.ModelSerializer):
    '''
        流程列表
    '''
    class Meta:
        model = ProcessApi
        fields = ('caseid', 'casename', 'identity', 'url','method','header','params',
                  'body','exceptres','result','belong','system','sortid','duration','head',
                  'isprocess','depend_id','depend_key','replace_key','replace_position')  # 需要序列化的属性

class AddProcessApiSerializers(serializers.ModelSerializer):
    '''
        新增流程接口
    '''
    class Meta:
        model = ProcessApi
        fields = ('caseid', 'casename', 'identity', 'url','method','params','body','belong','system',
                  'head','depend_id','depend_key','replace_key','replace_position')  # 需要序列化的属性

class ProcessApiParamsSerializers(serializers.ModelSerializer):
    '''
        流程接口-修改params的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('params',)  # 需要序列化的属性

class ProcessApiBodySerializers(serializers.ModelSerializer):
    '''
        流程接口-修改body的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('body',)  # 需要序列化的属性

class ProcessApiHeadSerializers(serializers.ModelSerializer):
    '''
        流程接口-修改负责人的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('head',)  # 需要序列化的属性

class ProcessApiDependKeySerializers(serializers.ModelSerializer):
    '''
        流程接口-修改依赖的键的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('depend_key',)  # 需要序列化的属性

class ProcessApiDependIdSerializers(serializers.ModelSerializer):
    '''
        流程接口-修改依赖id的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('depend_id',)  # 需要序列化的属性

class ProcessApiReplaceKeySerializers(serializers.ModelSerializer):
    '''
        流程接口-修改代替的key的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('replace_key',)  # 需要序列化的属性

class ProcessApiReplacePositionSerializers(serializers.ModelSerializer):
    '''
        流程接口-修改代替位置的值
    '''
    class Meta:
        model = ProcessApi
        fields = ('replace_position',)  # 需要序列化的属性

class ProcessApiResponseSerializers(serializers.ModelSerializer):
    '''
        流程接口，更新响应内容和响应延迟
    '''
    class Meta:
        model = ProcessApi
        fields = ('result','duration')  # 需要序列化的属性

###########################LocustApi####################################

class LocustApiSerializers(serializers.ModelSerializer):
    '''
        流程接口，更新响应内容和响应延迟
    '''
    class Meta:
        model = LocustApi
        fields = ('caseid', 'identity', 'url','method','params','body',"header","ip")  # 需要序列化的属性

###########################SingleApiChild####################################

class ParameterListSer(serializers.ModelSerializer):
    '''
        单一接口参数子表
    '''
    area = serializers.CharField(source="get_area_display")
    isMust = serializers.CharField(source="get_isMust_display")
    class Meta:
        model = SingleApiChild
        fields = ["id","parent_id","parameter_field","parameter_that","area","isMust","sample"]

class AddParameterSer(serializers.ModelSerializer):
    '''
        单一接口参数子表
    '''
    class Meta:
        model = SingleApiChild
        fields = ["parent_id","parameter_field","parameter_that","area","isMust","sample"]

class UpdateParameterSer(serializers.ModelSerializer):
    '''
        单一接口参数子表
    '''
    class Meta:
        model = SingleApiChild
        fields = ["parameter_field","parameter_that","area","isMust","sample"]


###########################functionCase####################################

class functionCaseSer(serializers.ModelSerializer):
    '''
        功能测试主表
    '''
    class Meta:
        model = FunctionCase
        fields = "__all__"

class functionCaseChildSer(serializers.ModelSerializer):
    '''
        功能测试主表
    '''
    class Meta:
        model = FunctionCaseChild
        fields = "__all__"
