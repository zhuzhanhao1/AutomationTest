# Create your views here.

from rest_framework import viewsets
from ApiTest.models import Link,Testurl
from ApiTest.serializers import LinkSerializers,TesturlSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LinkList(APIView):

    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 友情链接列表
        '''
        link_list = Link.objects.all()
        serializer = LinkSerializers(link_list, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})




class TesturlList(APIView):

    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 日常所需测试网址列表
        '''
        testurl_list = Testurl.objects.all()
        serializer = TesturlSerializers(testurl_list, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})

