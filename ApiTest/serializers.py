from rest_framework import serializers
from .models import SingleApi,LeftMenu,ChildMenu,SystemRole,Link,Testurl


class SingleApiSerializers(serializers.ModelSerializer):
    '''
        单一接口
    '''
    class Meta:
        model = SingleApi
        fields = ('caseid', 'casename', 'identity', 'url','method','header','params','body','exceptres','result','belong','system','sortid','duration','head')  # 需要序列化的属性

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


class LeftMenuSerializers(serializers.ModelSerializer):
    '''
        左侧一级菜单
    '''
    class Meta:
        model = LeftMenu
        fields = ('title','icon','href','spread')


class ChildMenuSerializers(serializers.ModelSerializer):
    '''
        二级自由菜单
    '''
    class Meta:
        model = ChildMenu
        fields = ('title','icon','href','spread')

class SystemRoleSerializers(serializers.ModelSerializer):
    '''
        系统角色
    '''
    class Meta:
        model = SystemRole
        fields = ('id','identity','role','username','password','token','system')

class TokenSerializers(serializers.ModelSerializer):
    '''
        更新令牌信息
    '''
    class Meta:
        model = SystemRole
        fields = ('token',)

class SystemRoleUpdateInfoSerializers(serializers.ModelSerializer):
    '''
        更新系统角色信息
    '''
    class Meta:
        model = SystemRole
        fields = ('username','password',)


class LinkSerializers(serializers.ModelSerializer):
    '''
        友情链接
    '''
    class Meta:
        model = Link
        fields = ('id', 'logo','websites','url')

class TesturlSerializers(serializers.ModelSerializer):
    '''
        测试网址
    '''
    class Meta:
        model = Testurl
        fields = ('id', 'logo','websites','url','apidocument')