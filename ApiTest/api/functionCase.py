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
        system = request.GET.get("system", "")
        if casename:
            if belong:
                apilists = FunctionCase.objects.filter(Q(casename__contains=casename) & Q(belong__contains=belong) & Q(system=system))
                if apilists.count() == 0:
                    caselist = FunctionCase.objects.filter(Q(execution_result__contains="failed")  & Q(system=system))
            else:
                apilists = FunctionCase.objects.filter(Q(casename__contains=casename) & Q(system=system))
                if  apilists.count() == 0:
                    caselist = FunctionCase.objects.filter(Q(result__contains="success")  & Q(system=system))

        elif system:
            if belong:
                caselist = FunctionCase.objects.filter(Q(belong__contains=belong) & Q(system=system))
            else:
                caselist = FunctionCase.objects.filter(system=system)
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
        '''
            创建功能用例-操作步骤、预计结果
        '''
        ret = {"code": 1000}
        try:
            data = request.data
            serializer = functionCaseSer(data=data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "添加成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "添加失败"
        return Response(ret)

    def get_object(self, pk):
        try:
            return FunctionCase.objects.get(id=pk)
        except FunctionCase.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        '''
            编辑功能用例-操作步骤、预计结果
        '''
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            serializer = functionCaseSer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
            删除功能用例-操作步骤、预计结果
        """
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            ret["msg"] = "删除成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除失败"
        return Response(ret)


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
        '''
            创建功能用例-操作步骤、预计结果
        '''
        ret = {"code": 1000}
        try:
            data = request.data
            serializer = functionCaseChildSer(data=data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "添加成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "添加失败"
        return Response(ret)

    def get_object(self, pk):
        try:
            return FunctionCaseChild.objects.get(id=pk)
        except FunctionCaseChild.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        '''
            编辑功能用例-操作步骤、预计结果
        '''
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            serializer = functionCaseChildSer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
            删除功能用例-操作步骤、预计结果
        """
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            ret["msg"] = "删除成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除失败"
        return Response(ret)