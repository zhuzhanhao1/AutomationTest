from django.db.models import Q
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from ApiTest.models import LeftMenu, ChildMenu
from ApiTest.serializers import LeftMenuSerializers, ChildMenuSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

data = {
    "contentManagement": [
        {
            "title": "ERMS测试分类",
            "icon": "&#xe6c9;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "快速测试",
            "icon": "&#xe631;",
            "href": "/web_quicktest/",
            "spread": False
        },
        {
            "title": "单一接口测试",
            "icon": "&#xe716;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "流程接口测试",
            "icon": "&#xe638;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "功能测试",
            "icon": "&#xe857;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "自动化测试",
            "icon": "&#xe628;",
            "href": "",
            "spread": False,
            "children": []
        }
    ],
    "memberCenter": [
        {
            "title": "Transfer测试分类",
            "icon": "&#xe6c9;",
            "href": "",
            "spread": False,
            "children": [
            ]
        },
        {
            "title": "快速测试",
            "icon": "&#xe631;",
            "href": "/web_quicktest/",
            "spread": False
        },
        {
            "title": "单一接口测试",
            "icon": "&#xe674;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "流程接口测试",
            "icon": "&#xe638;",
            "href": "",
            "spread": False,
            "children": [
            ]
        },
        {
            "title": "功能测试",
            "icon": "&#xe857;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "自动化测试",
            "icon": "&#xe628;",
            "href": "",
            "spread": False
        }
    ],
    "systemeSttings": [
        {
            "title": "测试网址",
            "icon": "&#xe631;",
            "href": "/web_linktest/",
            "spread": False
        },
        {
            "title": "友情链接",
            "icon": "&#xe64c;",
            "href": "/web_linklist/",
            "spread": False
        },
        {
            "title": "系统日志",
            "icon": "&#xe857;",
            "href": "//",
            "spread": False
        }
    ],
    "seraphApi": [
        {
            "title": "Tdr测试分类",
            "icon": "&#xe6c9;",
            "href": "",
            "spread": False,
            "children": [
            ]
        },
        {
            "title": "快速测试",
            "icon": "&#xe631;",
            "href": "/web_quicktest/",
            "spread": False
        },
        {
            "title": "单一接口测试",
            "icon": "&#xe674;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "流程接口测试",
            "icon": "&#xe638;",
            "href": "",
            "spread": False,
            "children": [

            ]
        },
        {
            "title": "功能测试",
            "icon": "&#xe857;",
            "href": "",
            "spread": False,
            "children": []
        },
        {
            "title": "自动化测试",
            "icon": "&#xe628;",
            "href": "",
            "spread": False
        }
    ]
}


class LeftMenuList(APIView):
    '''
    头部导航菜单
    '''
    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 头部导航菜单-dict格式
        '''
        leftmenu_erms = LeftMenu.objects.filter(area="erms")
        leftmenu_erms_serializer = LeftMenuSerializers(leftmenu_erms, many=True)
        leftmenu_systemeSttings = LeftMenu.objects.filter(area="systemeSttings")
        leftmenu_systemeSttings_serializer = LeftMenuSerializers(leftmenu_systemeSttings, many=True)
        left = {}
        left["erms"] = leftmenu_erms_serializer.data
        left["systemeSttings"] = leftmenu_systemeSttings_serializer.data
        return left

    def post(self, request, format=None):
        serializer = LeftMenuSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildMenuList(APIView):
    '''
    左侧导航菜单
    '''
    def get(self, request, format=None):
        '''
        :param request: 头部导航菜单返回的dict，将子菜单拼接上去
        :param format:
        :return:
        '''
        left = LeftMenuList().get(request, format=None)
        ermsapi = ChildMenu.objects.filter(classification__title="ERMS接口测试")
        ermsapi_erializer = ChildMenuSerializers(ermsapi, many=True)
        tdrapi = ChildMenu.objects.filter(classification__title="TDR接口测试")
        tdrapi_erializer = ChildMenuSerializers(tdrapi, many=True)
        left["erms"][1]['children'] = ermsapi_erializer.data
        left["erms"][2]['children'] = tdrapi_erializer.data
        return Response(left)

    def post(self, request, format=None):
        serializer = ChildMenuSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
