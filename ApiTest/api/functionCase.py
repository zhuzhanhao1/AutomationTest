import json
from django.db.models import Q
from ApiTest.models import FunctionCase,FunctionCaseChild
from ApiTest.serializers import functionCaseSer,functionCaseChildSer
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xlrd
from ApiTest.common.readExcel import ReadExcel

from django.db import transaction


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
                caselist = FunctionCase.objects.filter(Q(casename__contains=casename) & Q(belong__contains=belong) & Q(system=system))
                if caselist.count() == 0:
                    caselist = FunctionCase.objects.filter(Q(execution_result__contains="failed")  & Q(system=system))
            else:
                caselist = FunctionCase.objects.filter(Q(casename__contains=casename) & Q(system=system))
                if  caselist.count() == 0:
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


class FunctionCaseImport(APIView):
    '''
        导入测试用例数据
    '''

    def post(self, request, *args, **kwargs):
        '''
        :param request:
        :return: 导入数据
        '''
        ret = {"code": 1000}
        f = request.FILES.get('file')  # sheet名
        print(f)
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            params_list = ReadExcel().read_excel(f)
            print(params_list)
            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for rowVlaues in params_list:
                        dic = {
                            "belong":rowVlaues[0],
                            "function_model": rowVlaues[1],
                            "function_point": rowVlaues[2],
                            "casename": rowVlaues[3],
                            "premise_condition": rowVlaues[5],
                            "note":rowVlaues[9],
                            "system": "erms",
                        }
                        print(dic)
                        serializer = functionCaseSer(data=dic)
                        if serializer.is_valid():
                            serializer.save()
                            ret["msg"] = "导入成功"
                            # id = FunctionCase.objects.filter(Q(function_point=rowVlaues[2])&Q(casename=rowVlaues[3])).first().id
                            # steps_list = rowVlaues[6].split("\n")
                            # child_dic = {
                            #     "parent_id" :id,
                            #     "step_id":1,
                            #     "steps":rowVlaues[6],
                            #     "expected_results":rowVlaues[6]
                            # }
            except:
                ret["code"] = 1001
                ret["error"] = "解析excel文件或者数据插入错误"
            return Response(ret)
        else:
            ret["code"] = 1001
            ret["error"] = "所选文件必须是xlsx、xls格式"
            return Response(ret)