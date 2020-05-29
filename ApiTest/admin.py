from django.contrib import admin

# Register your models here.

from .models import SingleApi,LeftMenu,ChildMenu,SystemRole,\
    Testurl,Link,ProcessApi,FunctionCase,FunctionCaseChild  # 记得导包

# 注册medel类到admin的方式-@admin.register(SingleApi)
'''
    list_display:     指定要显示的字段
    search_fields:  指定搜索的字段
    list_filter:        指定列表过滤器
    ordering：       指定排序字段
'''
@admin.register(SingleApi)
class SingleApiAdmin(admin.ModelAdmin):
    list_display = ('caseid', 'casename', 'identity', 'url','method','header','params','body','belong','system','sortid','head')  # 在后台列表下显示的字段
    search_fields = ('casename',)
    list_filter = ('belong',)
    ordering = ("sortid",)

@admin.register(LeftMenu)
class LeftMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','icon','href','spread')  # 在后台列表下显示的字段
    search_fields = ('title',)

@admin.register(ChildMenu)
class ChildMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'classification','title','icon','href','spread')  # 在后台列表下显示的字段
    search_fields = ('title',)

@admin.register(SystemRole)
class SystemRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role','username','password','system','token')  # 在后台列表下显示的字段
    search_fields = ('role','username')

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo','websites','url')  # 在后台列表下显示的字段
    search_fields = ('websites',)

@admin.register(Testurl)
class TesturlAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo','websites','url','apidocument')  # 在后台列表下显示的字段
    search_fields = ('websites',)

@admin.register(ProcessApi)
class ProcrssApiAdmin(admin.ModelAdmin):
    list_display = ('caseid', 'casename', 'identity', 'url','method','header','params','body','belong','system','sortid','head')  # 在后台列表下显示的字段
    search_fields = ('casename',)
    list_filter = ('belong',)
    ordering = ("sortid",)


@admin.register(FunctionCase)
class FunctionCaseAdmin(admin.ModelAdmin):
    list_display = ("belong","function_model","function_point","casename","premise_condition","execution_result","note","executor")  # 在后台列表下显示的字段
    search_fields = ('casename',)
    list_filter = ('belong',)


@admin.register(FunctionCaseChild)
class FunctionCaseChildAdmin(admin.ModelAdmin):
    list_display = ("parent_id","steps","expected_results")
