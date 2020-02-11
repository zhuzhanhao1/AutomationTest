"""AutomationTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from ApiTest.api import renderHtml

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>\w+)/', include('ApiTest.urls')),

    # 返回页面
    url(r'^login/$', renderHtml.login_views),
    url(r'^logout/$', renderHtml.logout_views),
    url(r'^index/$', renderHtml.index_views),
    url(r'^home/$', renderHtml.home_views),
    url(r'^quicktest/$', renderHtml.quicktest_views),
    url(r'^singleapi/$', renderHtml.singleapi_views),
    url(r'^processapi/$', renderHtml.processapi_views),
    url(r'^detail/$', renderHtml.apiDetail_views),
    url(r'^link/$', renderHtml.link_views),
    url(r'^testurl/$', renderHtml.testurl_views),
    url(r'^systemlog/$', renderHtml.systemlog_views),
    url(r'test/$', renderHtml.test),
]
