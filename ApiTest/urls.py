from django.conf.urls import url
from ApiTest.api import singleApiList, systemRole, Menu, Link, processApiList, \
                        publicApi, ProcessApiTest, singleApiTest, pyechartExport

urlpatterns = [
    # 单一接口测试
    url(r'singleapi/list/$', singleApiList.SingleApiList.as_view()),
    url(r'singleapi/add_case/$', singleApiList.AddSingleApi.as_view()),
    url(r'singleapi/del_case/(?P<pk>[0-9]+)/$', singleApiList.DelSingleApi.as_view()),
    url(r'singleapi/update_case/(?P<pk>[0-9]+)/$', singleApiList.UpdateSingleApi.as_view()),
    url(r'singleapi/detail_case/(?P<pk>[0-9]+)/$', singleApiList.SingleApiDetail.as_view()),
    url(r'singleapi/search/$', singleApiList.SearchSingleApi.as_view()),
    url(r'singleapi/run/$', singleApiTest.SingleApiTest.as_view()),
    url(r'singleapi/repeatrun/$', singleApiTest.RepeatRunSingleApi.as_view()),
    url(r'singleapi/locust/(?P<pk>[0-9]+)/$', singleApiTest.LocustSingApi.as_view()),
    url(r'singleapi/close_locust/$', singleApiTest.LocustSingApi.as_view()),
    url(r'singleapi/quickrun/$', singleApiTest.RunQuickTest.as_view()),
    url(r'singleapi/export_report/$', pyechartExport.EchartExport.as_view()),
    #单一接口参数详情
    url(r'singleapi/parameter_details/$', singleApiList.SingleApiChildList.as_view()),
    url(r'singleapi/add_parameter/$', singleApiList.AddChildParameter.as_view()),
    url(r'singleapi/update_parameter/(?P<pk>[0-9]+)/$', singleApiList.UpdateChildParameter.as_view()),
    url(r'singleapi/del_parameter/(?P<pk>[0-9]+)/$', singleApiList.DelChildParameter.as_view()),

    # 流程接口测试
    url(r'processapi/list/$', processApiList.ProcessApiList.as_view()),
    url(r'processapi/add_case/$', processApiList.AddProcessApi.as_view()),
    url(r'processapi/del_case/(?P<pk>[0-9]+)/$', processApiList.DelProcessApi.as_view()),
    url(r'processapi/update_case/(?P<pk>[0-9]+)/$', processApiList.UpdateProcessApi.as_view()),
    url(r'processapi/run/$', ProcessApiTest.ProcessApiTest.as_view()),
    url(r'processapi/result_list/$', ProcessApiTest.ProcessApiResultTest.as_view()),

    # 公共方法
    url(r'publicapi/sort/$', publicApi.PublicApiSort.as_view()),
    url(r'publicapi/dingding/$', publicApi.PublicApiDingDingNotice.as_view()),
    url(r'publicapi/import_case/$', publicApi.PublicApiImport.as_view()),

    # 测试系统角色
    url(r'systemrole/list/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/add_role/$', systemRole.AddSystemRole.as_view()),
    url(r'systemrole/update_info/(?P<pk>[a-z]+)/$', systemRole.UpdateSystemRole.as_view()),
    url(r'systemrole/get_token_by_role/$', systemRole.GetTokenByRole.as_view()),

    # 菜单
    url(r'menu/list/$', Menu.MenuList.as_view()),

    # 友情链接
    url(r'link/list/$', Link.LinkList.as_view()),
    url(r'link/add_link/$', Link.LinkList.as_view()),
    url(r'link/update_link/(?P<pk>[0-9]+)/$', Link.LinkList.as_view()),

    # 测试网址
    url(r'testurl/list/$', Link.TesturlList.as_view()),
]
