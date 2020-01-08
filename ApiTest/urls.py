from django.conf.urls import url
from ApiTest.api import renderHtml,singleApiList,systemRole,Menu,\
    quickTest,singleApiTest,Link,systemLog,processApiList,ProcessApiTest,\
    publicApi
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'login/$', renderHtml.login_views),
    url(r'logout/$', renderHtml.logout_views),
    url(r'index/$', renderHtml.index_views),
    url(r'home/$', renderHtml.home_views),
    url(r'quicktest/$', renderHtml.quicktest_views),
    url(r'singleapi/$', renderHtml.singleapi_views),
    url(r'processapi/$', renderHtml.processapi_views),
    url(r'detail/$', renderHtml.apiDetail_views),
    url(r'link/$', renderHtml.link_views),
    url(r'testurl/$', renderHtml.testurl_views),

    url(r'singleapi/list/$', singleApiList.SingleApiList.as_view()),
    url(r'singleapi/search/$', singleApiList.SearchSingleApi.as_view()),
    url(r'singleapi/run/$', singleApiTest.SingleApiTest.as_view()),
    url(r'singleapi/repeatrun/$', singleApiTest.RepeatRunSingleApi.as_view()),
    url(r'singleapi/add_case/$', singleApiList.AddSingleApi.as_view()),
    url(r'singleapi/del_case/(?P<pk>[0-9]+)/$', singleApiList.DelSingleApi.as_view()),
    url(r'singleapi/update_case/(?P<pk>[0-9]+)/$', singleApiList.UpdateSingleApi.as_view()),
    url(r'singleapi/detail_case/(?P<pk>[0-9]+)/$', singleApiList.SingleApiDetail.as_view()),

    url(r'processapi/list/$', processApiList.ProcessApiList.as_view()),
    url(r'processapi/add_case/$', processApiList.AddProcessApi.as_view()),
    url(r'processapi/del_case/(?P<pk>[0-9]+)/$', processApiList.DelProcessApi.as_view()),
    url(r'processapi/update_case/(?P<pk>[0-9]+)/$', processApiList.UpdateProcessApi.as_view()),
    url(r'processapi/run/$', ProcessApiTest.ProcessApiTest.as_view()),
    url(r'processapi/result_list/$', ProcessApiTest.ProcessApiResultTest.as_view()),

    url(r'publicapi/sort/$', publicApi.PublicApiSort.as_view()),
    url(r'publicapi/dingding/$', publicApi.PublicApiDingDingNotice.as_view()),
    url(r'publicapi/import_case/$', publicApi.PublicApiImport.as_view()),

    url(r'systemrole/list/$', systemRole.SystemRoleList.as_view()),
    url(r'systemrole/update_info/(?P<pk>[a-z]+)', systemRole.UpdateSystemRole.as_view()),
    url(r'systemrole/get_token_by_role/$', systemRole.GetTokenByRole.as_view()),

    url(r'leftmenu/list/$', Menu.LeftMenuList.as_view()),
    url(r'childmenu/list/$', Menu.ChildMenuList.as_view()),

    url(r'quicktest/run/$', quickTest.RunQuickTest.as_view()),

    url(r'link/list/$', Link.LinkList.as_view()),
    url(r'Testurl/list/$', Link.TesturlList.as_view()),
    url(r'Testurl/list/$', Link.TesturlList.as_view()),



]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
# 返回一个 URL pattern 列表，其中包含附加到每个 URL pattern 的格式后缀模式