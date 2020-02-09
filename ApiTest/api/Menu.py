# Create your views here.

from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from ApiTest.models import LeftMenu, ChildMenu
from ApiTest.serializers import LeftMenuSerializers, ChildMenuSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LeftMenuList(APIView):
    '''
    头部导航菜单
    '''
    def get_level_one_menu(self):
        '''
        :param request:
        :param format:
        :return: 头部导航菜单-dict格式-一级菜单
        '''
        left = {}
        leftmenu_single = LeftMenu.objects.filter(area="single")
        leftmenu_single_serializer = LeftMenuSerializers(leftmenu_single, many=True)

        leftmenu_process = LeftMenu.objects.filter(area="process")
        leftmenu_process_serializer = LeftMenuSerializers(leftmenu_process, many=True)

        leftmenu_systemeSttings = LeftMenu.objects.filter(area="systemeSttings")
        leftmenu_systemeSttings_serializer = LeftMenuSerializers(leftmenu_systemeSttings, many=True)

        left["single"] = leftmenu_single_serializer.data
        left['process'] = leftmenu_process_serializer.data
        left["systemeSttings"] = leftmenu_systemeSttings_serializer.data
        return left

    def post(self, request, format=None):
        '''
        新建一级菜单
        :param request:
        :param format:
        :return:
        '''
        serializer = LeftMenuSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildMenuList(LeftMenuList):
    '''
    左侧二级菜单，继承一级菜单
    '''
    def get(self, request, format=None):
        '''
        :param request: 二级菜单参数，评级一级菜单
        :param format:
        :return:
        '''
        left = self.get_level_one_menu()
        # print(left)

        ermsapi = ChildMenu.objects.filter(classification__title="ERMS接口测试")
        ermsapi_erializer = ChildMenuSerializers(ermsapi, many=True)

        tdrapi = ChildMenu.objects.filter(classification__title="TDR接口测试")
        tdrapi_erializer = ChildMenuSerializers(tdrapi, many=True)

        ermsprocess = ChildMenu.objects.filter(classification__title="ERMS接口流程测试")
        ermsprocess_erializer = ChildMenuSerializers(ermsprocess, many=True)

        tdrprocess = ChildMenu.objects.filter(classification__title="TDR接口流程测试")
        tdrprocess_erializer = ChildMenuSerializers(tdrprocess, many=True)

        left["single"][1]['children'] = ermsapi_erializer.data
        left["single"][2]['children'] = tdrapi_erializer.data
        left['process'][0]['children'] = ermsprocess_erializer.data
        left['process'][1]['children'] = tdrprocess_erializer.data
        return Response(left)

    def post(self, request, format=None):
        '''
        新建二级菜单
        :param request:
        :param format:
        :return:
        '''
        serializer = ChildMenuSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

