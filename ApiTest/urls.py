from django.conf.urls import url
from ApiTest.api import singleApiList, systemRole, Menu, Link, processApiList, \
                        publicApi, ProcessApiTest, singleApiTest, functionCase

urlpatterns = [
    # 单一接口测试
    url(r'singleapi/list/$', singleApiList.SingleApiList.as_view()),
    url(r'singleapi/add_case/$', singleApiList.SingleApiList.as_view()),
    url(r'singleapi/del_case/(?P<pk>[0-9]+)/$', singleApiList.SingleApiList.as_view()),
    url(r'singleapi/update_case/(?P<pk>[0-9]+)/$', singleApiList.UpdateSingleApi.as_view()),
    url(r'singleapi/detail_case/(?P<pk>[0-9]+)/$', singleApiList.SingleApiDetail.as_view()),
    url(r'singleapi/search/$', singleApiList.SearchSingleApi.as_view()),
    url(r'singleapi/run/$', singleApiTest.SingleApiTest.as_view()),
    url(r'singleapi/repeatrun/$', singleApiTest.RepeatRunSingleApi.as_view()),
    url(r'singleapi/locust/(?P<pk>[0-9]+)/$', singleApiTest.LocustSingApi.as_view()),
    url(r'singleapi/close_locust/$', singleApiTest.LocustSingApi.as_view()),
    url(r'singleapi/quickrun/$', singleApiTest.RunQuickTest.as_view()),

    #单一接口参数详情
    url(r'singleapi/parameter_details/$', singleApiList.SingleApiChildList.as_view()),
    url(r'singleapi/add_parameter/$', singleApiList.SingleApiChildList.as_view()),
    url(r'singleapi/update_parameter/(?P<pk>[0-9]+)/$', singleApiList.SingleApiChildList.as_view()),
    url(r'singleapi/del_parameter/(?P<pk>[0-9]+)/$', singleApiList.SingleApiChildList.as_view()),
    url(r'singleapi/test/$', singleApiList.UpdateIdentity.as_view()),

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
    url(r'publicapi/export_report/$', publicApi.EchartExport.as_view()),

    # 测试系统角色
    url(r'systemrole/list/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/add_role/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/update_role/(?P<pk>[0-9]+)/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/del_role/(?P<pk>[0-9]+)/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/get_token_by_id/$', systemRole.SystemRoleToken.as_view()),
    url(r'systemrole/get_role_by_system/$', systemRole.SystemRoleToken.as_view()),

    # 菜单
    url(r'menu/list/$', Menu.MenuListManage.as_view()),
    url(r'menu/tree/$', Menu.MenuTree.as_view()),
    url(r'menu/table/$', Menu.MenuTableList.as_view()),
    url(r'menu/add_childmenu/$', Menu.MenuTableList.as_view()),
    url(r'menu/update_childmenu/(?P<pk>[0-9]+)/$', Menu.MenuTableList.as_view()),
    url(r'menu/del_childmenu/(?P<pk>[0-9]+)/$', Menu.MenuTableList.as_view()),
    url(r'menu/get_belong_by_system/$', Menu.MenuBelongParams.as_view()),

    # 友情链接
    url(r'link/list/$', Link.LinkList.as_view()),
    url(r'link/add_link/$', Link.LinkList.as_view()),
    url(r'link/update_link/(?P<pk>[0-9]+)/$', Link.LinkList.as_view()),
    url(r'link/del_link/(?P<pk>[0-9]+)/$', Link.LinkList.as_view()),

    # 测试网址
    url(r'testurl/list/$', Link.TesturlList.as_view()),
    url(r'testurl/add_test_url/$', Link.TesturlList.as_view()),
    url(r'testurl/update_test_url/(?P<pk>[0-9]+)/$', Link.TesturlList.as_view()),
    url(r'testurl/del_test_url/(?P<pk>[0-9]+)/$', Link.TesturlList.as_view()),

    #功能测试
    url(r'functioncase/list/$', functionCase.FunctionCaseList.as_view()),
    url(r'functioncase/add_case/$', functionCase.FunctionCaseList.as_view()),
    url(r'functioncase/update_case/(?P<pk>[0-9]+)/$', functionCase.FunctionCaseList.as_view()),
    url(r'functioncase/del_case/(?P<pk>[0-9]+)/$', functionCase.FunctionCaseList.as_view()),

    #功能测试子表
    url(r'functioncase/childlist/$', functionCase.FunctionCaseChildList.as_view()),
    url(r'functioncase/add_child/$', functionCase.FunctionCaseChildList.as_view()),
    url(r'functioncase/update_child/(?P<pk>[0-9]+)/$', functionCase.FunctionCaseChildList.as_view()),
    url(r'functioncase/del_child/(?P<pk>[0-9]+)/$', functionCase.FunctionCaseChildList.as_view()),
]
