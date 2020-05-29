import json
from django.db.models import Q
from ApiTest.models import FunctionCase,FunctionCaseChild
from ApiTest.serializers import functionCaseSer,functionCaseChildSer
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FunctionCaseList(APIView):
    """
    单一接口列表
    """
    def get(self, request, *args ,**kwargs):
        casename = request.GET.get("casename", "")          #搜索名字
        belong = request.GET.get("belong", "")              #所属模块
        system = request.GET.get("system", "")              #所属系统
        caselist = FunctionCase.objects.filter()
        serializer = functionCaseSer(caselist, many=True)
        pageindex = request.GET.get('page', 1)      # 页数
        pagesize = request.GET.get("limit", 30)     # 每页显示数量
        pageInator = Paginator(serializer.data, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})


    def post(self, request, *args, **kwargs):
        pass


    def put(self, request, pk, *args, **kwargs):
        pass

    def delete(self, request, pk, *args, **kwargs):
        pass


class FunctionCaseChildList(APIView):
    """
    单一接口列表
    """

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id","")
        queryset = FunctionCaseChild.objects.filter(parent_id_id=id)
        serializer = functionCaseChildSer(queryset, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, pk, *args, **kwargs):
        pass

    def delete(self, request, pk, *args, **kwargs):
        pass