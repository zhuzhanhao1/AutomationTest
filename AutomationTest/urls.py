from django.conf.urls import url,include
from django.contrib import admin
from ApiTest.api import renderHtml

urlpatterns = [
    #django-restframework
    url(r'^api/(?P<version>\w+)/', include('ApiTest.urls')),
    # 后台页面
    url(r'^admin/', admin.site.urls),
    # 返回页面
    url(r'^login/$', renderHtml.login_views),
    url(r'^dingding_login/$', renderHtml.dingding_login_views),
    url(r'^logout/$', renderHtml.logout_views),
    url(r'^index/$', renderHtml.index_views),
    url(r'^home/', renderHtml.home_views),
    url(r'^quicktest/$', renderHtml.quicktest_views),
    url(r'^singleapi/$', renderHtml.singleapi_views),
    url(r'^processapi/$', renderHtml.processapi_views),
    url(r'^detail/$', renderHtml.apiDetail_views),
    url(r'^link/$', renderHtml.link_views),
    url(r'^testurl/$', renderHtml.testurl_views),
    url(r'^systemlog/$', renderHtml.systemlog_views),
    url(r'^menu_management/$', renderHtml.menu_management_views),
    url(r'^echart_report/$', renderHtml.echart_report_views),
]
