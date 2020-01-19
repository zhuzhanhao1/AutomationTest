# Create your views here.
import json
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from ApiTest.models import ProcessApi
from ApiTest.serializers import ProcessApiListSerializers,AddProcessApiSerializers,\
    ProcessApiParamsSerializers,ProcessApiHeadSerializers,ProcessApiBodySerializers,\
    ProcessApiDependKeySerializers,ProcessApiDependIdSerializers,ProcessApiReplaceKeySerializers,\
    ProcessApiReplacePositionSerializers

from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProcessApiList(APIView):
    """
    单一接口列表
    """
    def get(self, request, format=None):
        casename = request.GET.get("casename", "")     #搜索名字
        belong = request.GET.get("belong", "")              #所属模块
        system = request.GET.get("system", "")              #所属系统
        if casename:
            if belong:
                apilists = ProcessApi.objects.filter(Q(casename__contains=casename) & Q(belong=belong) & Q(system=system))
                if apilists.count() == 0:
                    apilists = ProcessApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))
            else:
                apilists = ProcessApi.objects.filter(Q(casename__contains=casename) & Q(system=system))
                if  apilists.count() == 0:
                    apilists = ProcessApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))

        elif system:
            if belong:
                apilists = ProcessApi.objects.filter(Q(belong=belong) & Q(system=system)).order_by("sortid")
            else:
                apilists = ProcessApi.objects.filter(system=system).order_by("sortid")

        serializer = ProcessApiListSerializers(apilists, many=True)
        pageindex = request.GET.get('page', 1)  # 页数
        pagesize = request.GET.get("limit", 30)  # 每页显示数量
        pageInator = Paginator(serializer.data, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})


class AddProcessApi(APIView):
    '''
    创建单一接口
    '''
    def parameter_check(self):
        """
        验证参数
        """
        L = []
        all = ProcessApi.objects.all()
        for i in all:
            L.append(i.sortid)
        Newsordid = max(L) + 1
        return Newsordid

    def post(self, request, format=None):
        serializer = AddProcessApiSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(data={"code": "201", "msg": "操作成功"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProcessApi(APIView):
    """
    更新单一接口
    """
    def get_object(self, pk):
        try:
            print(pk)
            return ProcessApi.objects.get(caseid=pk)
        except ProcessApi.DoesNotExist:
            raise Http404


    def put(self, request, pk, format=None):
        '''
        :param request: 整理内容
        :param pk: 唯一id
        :param format:
        :return:
        '''
        snippet = self.get_object(pk)
        serializer = AddProcessApiSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"code": "201", "msg": "操作成功"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        '''
        :param request: 责任者
        :param pk: 唯一id
        :param format:
        :return:
        '''
        head = request.GET.get("head","")
        depend_key = request.GET.get("depend_key","")
        depend_id = request.GET.get("depend_id","")
        replace_key = request.GET.get("replace_key","")
        replace_position = request.GET.get("replace_position","")
        snippet = self.get_object(pk)

        if head:
            data = {"head":head}
            serializer = ProcessApiHeadSerializers(snippet, data=data)
        elif depend_id:
            data = {"depend_id":depend_id}
            serializer = ProcessApiDependIdSerializers(snippet, data=data)
        elif depend_key:
            data = {"depend_key":depend_key}
            serializer = ProcessApiDependKeySerializers(snippet, data=data)
        elif replace_key:
            data = {"replace_key": replace_key}
            serializer = ProcessApiReplaceKeySerializers(snippet, data=data)
        elif replace_position:
            if replace_position not in ["params","body"]:
                replace_position = None
            data = {"replace_position": replace_position}
            serializer = ProcessApiReplacePositionSerializers(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"code": "201", "msg": "操作成功"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, pk, format=None):
        '''
        :param request: params或者body
        :param pk: 唯一id
        :param format:
        :return: 如果是params则修改parmas的值，否则修改body的值
        '''
        snippet = self.get_object(pk)
        try:
            a = request.data["params"]
            print(a)
            serializer = ProcessApiParamsSerializers(snippet, data=request.data)
        except:
            serializer = ProcessApiBodySerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"code": "201", "msg": "操作成功"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DelProcessApi(APIView):
    """
    删除单一接口
    """
    def get_object(self, pk):
        try:
            return ProcessApi.objects.get(caseid=pk)
        except ProcessApi.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        #批量删除
        if pk == '0':
            for i in json.loads(request.data['ids']):
                self.get_object(i).delete()
            return Response({"code": "204", "msg": "操作成功"},status=status.HTTP_200_OK)
        #单个删除
        else:
            snippet = self.get_object(pk)
            snippet.delete()
            return Response({"code": "204", "msg": "操作成功"},status=status.HTTP_200_OK)